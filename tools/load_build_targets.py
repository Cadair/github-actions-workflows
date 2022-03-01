import json

import click
import yaml

MACHINE_TYPE = {
    "linux": "ubuntu-20.04",
    "macos": "macos-10.15",
    "windows": "windows-2019",
}


@click.command()
@click.option("--targets", default="")
def load_build_targets(targets):
    """Script to load cibuildwheel targets for GitHub Actions workflow."""
    # Load list of targets
    targets = yaml.load(targets, Loader=yaml.BaseLoader)
    print(json.dumps(targets, indent=2))

    # Create matrix
    matrix = {"include": []}
    for target in targets:
        matrix["include"].append(get_matrix_item(target))

    # Output matrix
    print(json.dumps(matrix, indent=2))
    print(f"::set-output name=matrix::{json.dumps(matrix)}")


def get_os(target):
    if "macos" in target:
        return MACHINE_TYPE["macos"]
    if "win" in target:
        return MACHINE_TYPE["windows"]
    return MACHINE_TYPE["linux"]


def get_cibw_build(target):
    if target in {"linux", "macos", "windows"}:
        return ""
    return target


def get_cibw_archs(target):
    for arch in ["aarch64", "arm64", "universal2"]:
        if target.endswith(arch):
            return arch
    return ""


def get_matrix_item(target):
    return {
        "target": target,
        "os": get_os(target),
        "CIBW_BUILD": get_cibw_build(target),
        "CIBW_ARCHS": get_cibw_archs(target),
    }


if __name__ == "__main__":
    load_build_targets()
