# -*- coding: utf-8 -*-

"""Console script for imports."""
import sys
import click

import imports


@click.command()
@click.argument('path_dir')
def main(path_dir):
    """Console script for imports."""
    click.echo("Replace this message by putting your code into "
               "imports.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return imports.check(path_dir)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
