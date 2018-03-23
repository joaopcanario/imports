# -*- coding: utf-8 -*-

"""Console script for imports."""
import sys
import click

from imports.imports import check


@click.command()
@click.argument('path_dir')
@click.argument('requirements_name', default='requirements.txt')
def main(path_dir, requirements_name):
    """Console script for imports."""
    click.echo("\nWARNING: Uninstall libs it's at your own risk!")
    click.echo('\nREMINDER: After uninstall libs, update your requirements '
               'file.\nUse the `pip freeze > requirements.txt` command.')

    click.echo('\n\nList of installed libs and your dependencies added on '
               'project\nrequirements that are not being used:\n')

    check(path_dir, requirements_name)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
