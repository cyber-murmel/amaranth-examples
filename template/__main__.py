from amaranth import *
from amaranth_boards.utils import *
from amaranth.cli import main_parser, main_runner
from argparse import ArgumentParser
from .template import Top


def extra_options():
    parser = ArgumentParser()
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

    if plat:
        clk_frequency = plat.default_clk_frequency
    elif "simulate" == args.action:
        clk_frequency = 1 / args.sync_period
    else:
        # "generate" == args.action
        clk_frequency = 1e6

    top = Top(
        clk_frequency=clk_frequency,
    )

    if args.action:
        main_runner(
            parser=parser,
            args=args,
            design=top,
            platform=plat,
            ports=top.ports,
        )
    elif plat:
        plat.build(top, do_program=True)
    else:
        print(f"Please run 'simulate' or 'generate', or set '--platform'.")
