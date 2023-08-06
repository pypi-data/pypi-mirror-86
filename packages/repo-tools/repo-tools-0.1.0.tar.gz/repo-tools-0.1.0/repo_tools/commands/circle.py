#!/usr/local/bin/python

"""
This command will reverse the action of circleci config pack.
It's following the fyaml specification: https://github.com/CircleCI-Public/fyaml/blob/master/fyaml-specification.md
"""
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import typer
from ruamel.yaml import YAML

from repo_tools.common import utils

circle_app = typer.Typer()

TOP_LEVEL_KEYS = ["version", "description", "display", "orbs", "parameters"]


@circle_app.command()
def explode(
    path: Optional[str] = typer.Argument(".", help="path to the circle ci config"),
    out: Optional[str] = typer.Option("./.circleci/config/", help="output directory"),
):
    if not path.endswith(".yml"):
        utils.exit_cli("path must be a yml file", 1)

    path_to_file = os.path.abspath(os.path.join(os.getcwd(), path))
    output_full_path = os.path.abspath(os.path.join(os.getcwd(), out))

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True

    with tempfile.TemporaryDirectory() as temp_dir:
        file_tree = generate_file_tree(yaml, path_to_file, output_dir=temp_dir)
        _create_file_tree(yaml, file_tree)
        shutil.copytree(temp_dir, output_full_path)


def generate_file_tree(yaml: YAML, path: str, output_dir: str):

    data = yaml.load(Path(path))

    files_to_be_created = dict()

    at_file = dict({key: value for key, value in data.items() if key in TOP_LEVEL_KEYS})
    files_to_be_created.update({os.path.join(output_dir, "@config.yml"): at_file})

    configuration = dict(
        {key: value for key, value in data.items() if key not in TOP_LEVEL_KEYS}
    )
    for key, value in configuration.items():
        temp_file_path = os.path.join(output_dir, key)
        for _key, _value in value.items():
            if isinstance(_value, dict):
                files_to_be_created.update(
                    {os.path.join(temp_file_path, f"{_key}.yml"): _value.items()}
                )
            else:
                files_to_be_created.update(
                    {os.path.join(temp_file_path, f"@{_key}.yml"): {_key: _value}}
                )

    return files_to_be_created


def _create_file_tree(yaml, files_to_be_created):
    for path, content in files_to_be_created.items():
        os.makedirs(path.rsplit("/", 1)[0], exist_ok=True)
        with open(path, "w+") as file:
            yaml.dump(dict(content), file)
