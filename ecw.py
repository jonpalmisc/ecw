#!/usr/bin/env python3

# Copyright (c) 2022 Jon Palmisciano
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from enum import Enum
import os
from pathlib import Path
import subprocess
import shutil
from typing import Optional, List


class BuildMode(str, Enum):
    """
    Types of CMake build modes.
    """

    debug = "d"
    release = "r"
    release_with_debug = "w"
    min_size_release = "s"

    def to_param(self) -> str:
        """
        Convert a build mode to a CMAKE_BUILD_TYPE parameter.
        """

        if self == BuildMode.release:
            return "Release"
        elif self == BuildMode.release_with_debug:
            return "RelWithDebInfo"
        elif self == BuildMode.min_size_release:
            return "MinSizeRel"

        return "Debug"


def call(command: List[str], quiet: bool = False):
    """
    Call (and echo) a shell command, optionally echoing the output.
    """

    typer.echo(f"> {' '.join(command)}")

    if quiet:
        result = subprocess.call(command, stdout=open(os.devnull, "wb"))
    else:
        result = subprocess.call(command)

    if result != 0:
        raise typer.Exit(result)


import typer

app = typer.Typer(
    add_completion=False,
    help="Use CMake more efficiently.",
    no_args_is_help=True,
    context_settings=dict(max_content_width=90),
)


@app.command()
def config(
    cmake_params: Optional[List[str]] = typer.Argument(
        None, help="Additional parameters to pass to CMake."
    ),
    source_dir: Path = typer.Option(
        ".",
        "--source-dir",
        "-S",
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
        metavar="PATH",
        help="Path to source root.",
    ),
    build_dir: Path = typer.Option(
        "build",
        "--build-dir",
        "-B",
        file_okay=False,
        readable=True,
        writable=True,
        resolve_path=True,
        metavar="PATH",
        help="Path to build root.",
    ),
    mode: Optional[BuildMode] = typer.Option(
        BuildMode.debug,
        "--mode",
        "-M",
        help="Type of build to configure.",
    ),
    export_cc: bool = typer.Option(
        False,
        "--export-cc",
        "-E",
        help="Enable generation of 'compile_commands.json'.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Silence output from CMake during configuration.",
    ),
    reset: bool = typer.Option(
        False,
        "--reset",
        "-R",
        help="Re-create the build root if it already exists.",
    ),
):
    """
    Configure a CMake project.
    """

    # Reset the build directory if requested.
    if reset:

        # Prevent accidental source code removal due to swapped directories.
        if build_dir in source_dir.parents:
            return typer.echo(
                "Error: Build root contains source root; cannot remove.", err=True
            )
        elif os.path.isdir(build_dir):
            shutil.rmtree(build_dir)

    command = ["cmake", "-S", str(source_dir), "-B", str(build_dir)]
    if mode:
        command += ["-DCMAKE_BUILD_TYPE=" + mode.to_param()]
    if export_cc:
        command += ["-DCMAKE_EXPORT_COMPILE_COMMANDS=1"]
    if cmake_params:
        command += cmake_params

    call(command, quiet)


@app.command()
def build(
    target: str = typer.Argument("all", help="Name of the target to build."),
    build_dir: Path = typer.Option(
        "build",
        "--build-dir",
        "-B",
        file_okay=False,
        readable=True,
        writable=True,
        resolve_path=True,
        metavar="PATH",
        help="Path to build root.",
    ),
):
    """
    Build the CMake project in the current directory.
    """

    command = ["cmake", "--build", str(build_dir)]
    if target != "all":
        command += ["-t", target]

    call(command)


if __name__ == "__main__":
    app()
