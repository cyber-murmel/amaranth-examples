# Amaranth Examples

This repository is based on [icebreaker-amaranth-examples](https://github.com/icebreaker-fpga/icebreaker-amaranth-examples) and contains examples for the [Amaranth hardware definition language](https://github.com/amaranth-lang/amaranth)
Python library for register transfer level modeling of synchronous logic. Ordinary Python code is used to construct a netlist of a digital circuits, which can be simulated, directly synthesized via Yosys, or converted to human-readable Verilog code for use with industry-standard toolchains.

## Setup
Clone this repository recursively.

```shell
git clone https://github.com/cyber-murmel/amaranth-examples.git
cd amaranth-examples
```

If you just want to let the rubber hit the road, there is a [TL;DR](README.md#tldr) at the bottom of this readme.

### Toolchain
To synthesize and upload bitstrams you need to install
[`yosys`](https://yosyshq.net/yosys/download.html),
[`icestorm`](https://clifford.at/icestorm),
[`nextpnr`](https://github.com/YosysHQ/nextpnr) and
[`libus`](https://libusb.info/).
These packages should be available for most common Linux distributions. If that's not the case, click the link to the respective package above.

#### Python
Install the necessary Python packages from the `reuqirements.txt`. I recommend using Python venv.

```shell
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip --requirement requirements.txt
```

When you are done with the project simply close the shell or run `deactivate` to exit the venv. You need to run `source .venv/bin/activate` from the root of this repository when you want to use this project in a new shell.

#### Formal Verification
If you want to get started with formal verification, you also need to install [`symbiyosys` and `yices`](https://symbiyosys.readthedocs.io/en/latest/install.html).

#### Nix(OS)
Users of Nix or NixOS can skip the toolchain instructions above and simply run `nix-shell` in the root of this directory to drop into a functional development environment.

## Warning
Amaranth is still a work in progress project. Expect examples to occasionally break until amaranth fully stabilizes.

## Usage
The examples in this repository are structured as executable python modules and can be run with `python3 -m modulename`. Run this with `--help` to get specific usage information to each module.

```shell
python3 -m blink --help
```

### Simulation
To run a module virtually, call the module with the `simulate` command, and specify the number of clock cycles to run and the paths for the VCD and GTKW file.

```shell
python3 -m blink \
  simulate \
    --clocks 100 \
    --vcd-file blink.vcd \
    --gtkw-file blink.gtkw
```

To view the waveforms install and run [`gtkwave`](http://gtkwave.sourceforge.net/).

```shell
gtkwave --dump blink.vcd --save blink.gtkw
```

### Formal Verification
To get a quick understanding what formal verification is and what it can do, I recommend watching [Matt Venn's](https://www.youtube.com/watch?v=_5R35QFsXM4) or [Robert Beruch's](https://www.youtube.com/watch?v=9e7F1XhjhKw) video (series) or reading the [Wikipedia entry](https://en.wikipedia.org/wiki/Formal_verification).


Currently the only example with formal verification is [blink](blink/). Formal verification runs are implemented as Python [unit test cases](blink/tests/test_blink.py). Start formal verification by calling the `unittest` module with the blink module as argument.

```shell
python -m unittest blink
```

### Programming
To program an FPGA board, supply the `--platform` parameterto the module call. To get a list of available boards, call with the `--help` parameter.

```shell
python -m blink -p ICEBreaker
```

## TL;DR
MAKE BOARD BLINK NOW!!!11!!111!

```shell
# install required OS packages (choose your flavor)
# Debian
sudo apt install yosys fpga-icestorm nextpnr libusb
# Arch (AUR)
sudo yay -S yosys icestorm-git  nextpnr-git libusb

# get examples and mch2022-tools
git clone https://github.com/cyber-murmel/amaranth-examples.git
cd amaranth-examples

# install required python packages
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip --requirement requirements.txt

# test board
python -m blink -p ICEBreaker
```
