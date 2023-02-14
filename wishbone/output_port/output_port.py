from math import ceil, log2
from amaranth import *
from amaranth_soc.wishbone import *


class OuputPort(Elaboratable, Interface):
    def __init__(self, data_width, granularity=None):
        self.size = 1
        Interface.__init__(
            self,
            data_width=data_width,
            granularity=granularity,
            addr_width=ceil(log2(self.size + 1)),
        )
        self.out = Signal(self.data_width)

    def elaborate(self, platform) -> Module:
        m = Module()
        m.d.comb += [
            self.ack.eq(self.stb),
            self.out.eq(self.dat_r),
        ]
        with m.If(self.stb & self.we):
            if self.data_width == self.granularity:
                # select lines can be ignored
                m.d.sync += [self.dat_r.eq(self.dat_w)]
            else:
                for i, sel in enumerate(self.sel):
                    with m.If(sel):
                        dat_r_slice, dat_w_slice = (
                            signal.word_select(i, self.granularity)
                            for signal in (self.dat_r, self.dat_w)
                        )
                        m.d.sync += [dat_r_slice.eq(dat_w_slice)]
        return m

    @property
    def ports(self):
        return [self.cyc, self.stb, self.sel, self.we, self.dat_w, self.ack, self.dat_r]


class Top(Elaboratable):
    def __init__(self, period=2):
        half_period = int(period / 2) - 1  # one cycle needed for interface handshake
        self.half_period = 0 if half_period < 0 else half_period
        self.output_port = OuputPort(8)
        self.blink_out = Signal(1)
        self.fsm = None
        self.counter = Signal(range(self.half_period))

    @property
    def ports(self):
        return self.output_port.ports + [
            self.blink_out,
            # self.fsm,
            self.counter,
        ]

    def elaborate(self, platform) -> Module:
        m = Module()

        m.submodules.output_port = self.output_port

        m.d.comb += [self.blink_out.eq(self.output_port.out[0])]

        with m.FSM(reset="COUNT_DOWN") as self.fsm:
            with m.State("COUNT_DOWN"):
                with m.If(self.counter == 0):
                    # start cycle
                    m.d.sync += [
                        self.output_port.cyc.eq(1),
                        self.output_port.sel.eq(0),
                        self.output_port.dat_w.eq(1 - self.output_port.out),
                        self.output_port.stb.eq(1),
                        self.output_port.we.eq(1),
                    ]
                    m.next = "WAIT_FOR_ACK"
                with m.Else():
                    m.d.sync += self.counter.eq(self.counter - 1)
            with m.State("WAIT_FOR_ACK"):
                with m.If(self.output_port.ack):
                    m.d.sync += [
                        self.counter.eq(self.half_period - 1),
                        self.output_port.cyc.eq(0),
                        self.output_port.sel.eq(0),
                        self.output_port.dat_w.eq(0),
                        self.output_port.stb.eq(0),
                        self.output_port.we.eq(0),
                    ]
                    m.next = "COUNT_DOWN"

        if platform:
            ledg_n = platform.request("led")
            m.d.comb += [ledg_n.eq(self.blink_out)]

        return m
