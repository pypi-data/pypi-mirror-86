from __future__ import annotations
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

from git import Repo
import typer

from .models import Package, OutputMode
from .visitor import parse
from .helpers import find_modules, resolve_module_name

mode_help = dedent(
    """
    Output mode, one of "file" | "directory" | "stdout".
    For "file" and "stdout" the template receives a Package object and is written to
    "output" or echoed standardoutput. For "directory", the template receives one
    Module object per module and is written to one file per module, with the output
    directory structure mimicking the package structure. Defaults to "stdout"
    """
)


def process_package(package_root: Path) -> Package:
    if not package_root.exists():
        typer.echo(f"{str(package_root)} does not exist")
        typer.Exit(code=1)
    module_paths = find_modules(package_root)
    modules = [
        parse(module_path, resolve_module_name(module_path, package_root))
        for module_path in module_paths
    ]
    return Package(
        name=resolve_module_name(package_root, package_root), _modules=modules
    )


app = typer.Typer(
    help=dedent(
        """
    Extract docstrings from a python package and render them in a custom template.
    Docstring extraction is performed statically, meaning that your code is not being imported
    or run, so there is no need to worry about side effects.
    """
    )
)


@app.command()
def remote(
    uri: str = typer.Argument(
        ..., help="a git uri from which to fetch a remote git repo"
    ),
    template_file: Path = typer.Option(
        Path("template.md"), "--template-file", "-t", help="path to a Jinja2 template"
    ),
    output: Path = typer.Option(
        Path("build"), "--output", "-o", help="where to write the output to"
    ),
    package_root: Path = typer.Option(
        Path("src"),
        "--package-root",
        "-p",
        help="the relative path to the package root inside the repo",
    ),
    mode: OutputMode = typer.Option(
        OutputMode.stdout.value, "--mode", "-m", help=mode_help
    ),
):
    """Fetch a remote git repo, extract docstrings and render a template"""
    with TemporaryDirectory() as tmp_dir:
        directory = Path(Repo.clone_from(uri, tmp_dir).working_dir) / package_root
        package = process_package(directory)
        mode.apply(package, output, template_file)


@app.command()
def local(
    directory: Path = typer.Argument(Path("."), help="path to the package"),
    template_file: Path = typer.Option(
        Path("template.md"), "--template-file", "-t", help="path to a Jinja2 template"
    ),
    output: Path = typer.Option(
        Path("build"), "--output", "-o", help="where to write the output to"
    ),
    mode: OutputMode = typer.Option(
        OutputMode.stdout.value, "--mode", "-m", help=mode_help
    ),
):
    """Extract docstrings from a local package and render a template"""
    package = process_package(directory)
    mode.apply(package, output, template_file)


if __name__ == "__main__":
    app()
