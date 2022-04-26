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


from pathlib import Path
import subprocess
from typing import Optional, List

import typer

app = typer.Typer(add_completion=False)


def call(command: List[str]):
    typer.echo(f"> {' '.join(command)}")
    subprocess.call(command)


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
):
    """
    Configure a CMake project.
    """

    command = ["cmake", "-S", str(source_dir), "-B", str(build_dir)]
    if cmake_params:
        command += cmake_params

    call(command)


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
