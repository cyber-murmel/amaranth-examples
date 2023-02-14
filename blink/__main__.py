import argparse
from .blink import Blinker, Top
from amaranth import *
from amaranth.asserts import *
from amaranth_boards.utils import *
from amaranth.cli import main_parser, main_runner


def extra_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--blink-freq", type=float, default=1, help="blink frequency"
    )
    parser.add_argument(
        "-p",
        "--platform",
        choices=get_platform_names(),
        help="platform in use",
    )
    return parser


if __name__ == "__main__":
    parser = main_parser(extra_options())
    args = parser.parse_args()
    plat = (
        None
        if not args.platform in get_platform_names()
        else get_platform_by_name(args.platform)()
    )

    if args.action:
        sync = ClockDomain()
        top = Top(8)

        m = Module()
        m.domains += sync
        m.submodules += top

        main_runner(
            parser=parser,
            args=args,
            design=m,
            platform=plat,
            ports=[
                sync.clk,
                sync.rst,
            ]
            + top.ports,
        )
    elif plat:
        top = Top(period=plat.default_clk_frequency / args.blink_freq)
        plat.build(top, do_program=True)
    else:
        print(f"Please run 'simulate' or 'generate', or set '--platform'.")
