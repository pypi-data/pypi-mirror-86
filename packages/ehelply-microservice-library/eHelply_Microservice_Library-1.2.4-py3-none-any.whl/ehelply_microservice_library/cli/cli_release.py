import typer
from pathlib import Path
from typing import List, Optional
from ehelply_bootstrapper.utils.state import State
from ehelply_bootstrapper.cli.releases import ReleasesConfig, ReleaseDetails, Releaser
import glob
import os

cli = typer.Typer()


@cli.command()
def create(version: str = typer.Option(..., prompt=True), name: str = typer.Option(..., prompt=True),
           releases: Optional[Path] = typer.Option(None)):
    base_path: Path = releases
    if not base_path:
        base_path = Path(os.getcwd())

    repo_path: Path = base_path  # Path(Path(__file__).resolve().parents[3])  # TODO: Change back to 3 (4 when testing in template)

    releases_path: Path = base_path.joinpath("releases.json")

    config: ReleasesConfig = ReleasesConfig(
        repo_path=repo_path,
        releases_path=releases_path
    )

    releaser: Releaser = Releaser(config)
    releaser.make(ReleaseDetails(name=name, version=version))


if __name__ == '__main__':
    cli()
