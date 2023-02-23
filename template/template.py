from amaranth import *


class Template(Elaboratable):
    def __init__(self):
        ...

    @property
    def ports(self):
        return []

    def elaborate(self, platform) -> Module:
        m = Module()

        # formal description of behavior
        if "formal" == platform:
            ...

        # definition of behavior
        m.d.comb += []
        m.d.sync += []

        return m


class Top(Elaboratable):
    def __init__(self, clk_frequency):
        # for simulation
        self.clock = Signal(1)

        self.template = Template()

    @property
    def ports(self):
        return [
            # for simulation
            self.clock,
        ]
        +self.template.ports

    def elaborate(self, platform):
        m = Module()

        m.d.comb += [
            # for simulation
            self.clock.eq(ClockSignal()),
        ]

        m.submodules.template = self.template

        if platform:
            # platform dependent connections
            ...

        return m
