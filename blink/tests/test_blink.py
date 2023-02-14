from ..blink import Blinker
from amaranth.test.utils import FHDLTestCase

period = 10


class BlinkTestCase(FHDLTestCase):
    def test_bmc(self):
        self.assertFormal(Blinker(period), mode="bmc", depth=4 * period)

    def test_cover(self):
        self.assertFormal(Blinker(period), mode="cover", depth=4 * period)

    def test_prove(self):
        self.assertFormal(Blinker(period), mode="prove", depth=4 * period)
