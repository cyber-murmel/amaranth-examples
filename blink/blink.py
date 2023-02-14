from amaranth import *
from amaranth.asserts import *


class Blinker(Elaboratable):
    def __init__(self, period=2):
        self.half_period = int(period / 2)
        self.blink_out = Signal(1)
        self.counter = Signal(range(self.half_period))

    @property
    def ports(self):
        return [
            self.blink_out,
            self.counter,
        ]

    def elaborate(self, platform) -> Module:
        m = Module()

        # Formal Description Of Behavior
        if "formal" == platform:
            # use register to count clock cycles
            ticks = Signal(32)
            m.d.sync += [
                ticks.eq(ticks + 1),
            ]

            m.d.comb += [
                # assert counter stays in range
                Assert(self.counter < self.half_period),
                Cover(self.blink_out == 1),
                Cover(self.blink_out == 0),
            ]

            # let run for one blink cycle
            with m.If(ticks > 2 * self.half_period):
                # check that blink frequency is correct
                m.d.comb += [
                    Assert(self.blink_out != Past(self.blink_out, self.half_period)),
                    Assert(
                        self.blink_out == Past(self.blink_out, 2 * self.half_period)
                    ),
                ]

                # counter reaches 0
                with m.If(Past(self.counter) == 0):
                    m.d.comb += [
                        # assert counter gets reset and LED flips
                        Assert(self.counter == self.half_period - 1),
                        Assert(self.blink_out != Past(self.blink_out)),
                    ]
                with m.Else():
                    m.d.comb += [
                        # assert that counter is counting and LED keeps state
                        Assert(self.counter == Past(self.counter) - 1),
                        Assert(self.blink_out == Past(self.blink_out)),
                    ]

        # Definition of Behavior
        with m.If(self.counter == 0):
            m.d.sync += [
                self.blink_out.eq(~self.blink_out),
                self.counter.eq(
                    self.half_period - 1
                ),  # one extra cycle is need for reloading the value
            ]
        with m.Else():
            m.d.sync += self.counter.eq(self.counter - 1)

        return m


class Top(Elaboratable):
    def __init__(self, period=2):
        self.blinker = Blinker(period)

    @property
    def ports(self):
        return self.blinker.ports

    def elaborate(self, platform):
        m = Module()

        m.submodules.blinker = self.blinker

        if platform:
            ledg_n = platform.request("led")
            m.d.comb += [ledg_n.eq(self.blinker.blink_out)]

        return m
