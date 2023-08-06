import sys
import click

from excelkit import version_info
from ._parse import parse_cli
from ._build import build_cli
from ._concat import concat_cli


__epilog__ = click.style('contact: {author} <{author_email}>'.format(**version_info), bold=True)
desc = click.style(version_info['desc'], bold=True, fg='cyan')

@click.group(epilog=__epilog__, help=desc)
@click.version_option(
    version=version_info['version'],
    prog_name=version_info['prog'],
    message=click.style('%(prog)s, %(version)s [{}]'.format(version_info['build_time']), fg='bright_green')
)
def cli():
    pass


def main():
    cli.add_command(parse_cli)
    cli.add_command(build_cli)
    cli.add_command(concat_cli)
    cli()


if __name__ == '__main__':
    main()
