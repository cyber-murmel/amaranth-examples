from ..template import Template
from amaranth.test.utils import FHDLTestCase

depth = 10


class TemplateTestCase(FHDLTestCase):
    def test_bmc(self):
        self.assertFormal(Template(), mode="bmc", depth=depth)

    def test_cover(self):
        self.assertFormal(Template(), mode="cover", depth=depth)

    def test_prove(self):
        self.assertFormal(Template(), mode="prove", depth=depth)
