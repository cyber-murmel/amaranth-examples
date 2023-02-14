{
  pkgs ?
  import (builtins.fetchGit {
    name = "nixos-22.11-2022_12_03";
    url = "https://github.com/nixos/nixpkgs/";
    ref = "refs/heads/nixos-22.11";
    rev = "660e7737851506374da39c0fa550c202c824a17c";
  }) {}
}:

with pkgs;
let
  amaranth-boards-chubbyhat = python3Packages.amaranth-boards.overrideAttrs (old: {
    pname = "amaranth_boards";
    version = "0.1";
    realVersion = "0.1.dev210+g${lib.substring 0 7 amaranth-boards-chubbyhat.src.rev}";
    src = fetchFromGitHub {
      owner = "cyber-murmel";
      repo = "amaranth-boards";
      rev = "fdd0038e1bd03021961923ef10f6ffee6cbc17f7";
      hash = "sha256-3p0Fx7gzxGQPy+FfHt9sQKW+q2hqXz6BeOvUGsG1kKg=";
    };
    pythonImportsCheck = [ "${amaranth-boards-chubbyhat.pname}" ];
  });
  apollo_fpga = with python3Packages; buildPythonPackage rec {
    pname = "apollo_fpga";
    version = "0.0.5";
    # python setup.py --version
    realVersion = "r0.0";

    src = fetchFromGitHub {
      owner = "greatscottgadgets";
      repo = "apollo";
      rev = "e0feb55e9c19ef113877c87b428cc5fb658af88d";
      hash = "sha256-V3DxblZBJnrjgsBvrkJS7VTr+mULmLcCz8ZsEuqh1TI=";
    };
    nativeBuildInputs = [
      git
      setuptools-scm
    ];
    propagatedBuildInputs = [
      pyusb
      pyvcd
      setuptools
      prompt-toolkit
    ];
    doCheck = false;
  };
in
mkShell {
  buildInputs = [
    (python3.withPackages (ps: with ps;[
      black
      pyusb
      pyserial
      amaranth
      amaranth-soc
      amaranth-boards-chubbyhat
      apollo_fpga
      jinja2
    ]))
    yosys
    icestorm nextpnr trellis
    gtkwave
    symbiyosys boolector yices
  ];
}
