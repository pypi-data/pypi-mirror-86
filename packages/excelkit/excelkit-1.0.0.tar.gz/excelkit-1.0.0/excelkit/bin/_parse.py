import sys
import click

from excelkit.core.parse import ExcelParser
from excelkit.util.reformat import Formatter

parse_examples = click.style('''
examples:

    excel-parse demo.xlsx

    excel-parse demo.xlsx -o out.tsv

    excel-parse demo.xlsx -O table

    excel-parse demo.xlsx -O table --color red

    excel-parse demo.xlsx -O json --indent 2

    excel-parse demo.xlsx -O json --indent 2 --header

    excel-parse demo.xlsx --pager
''', fg='yellow')

@click.command(name='parse', epilog=parse_examples, help=click.style('parse excel file', fg='bright_magenta', bold=True))
@click.argument('filename')
@click.option('-o', '--outfile', help='the output filename [stdout]')
@click.option('-O', '--outfmt',
              help='the format of output',
              type=click.Choice(['table', 'html', 'json', 'tsv']),
              default='tsv')
@click.option('--skip', help='skip the first N rows', type=int)
@click.option('--limit', help='limit N rows to output', type=int)
@click.option('--sheet', help='select an index of sheets', type=int)
@click.option('--indent', help='the indent size for json output', type=int)
@click.option('--sep', help='the separator for tsv output', default='\t')
@click.option('--index', help='show index of row for table output', is_flag=True)
@click.option('--header', help='use first row as header', is_flag=True)
@click.option('--pager', help='echo via pager', is_flag=True)
@click.option('--read-only', help='open excel in read-only mode, for large file', is_flag=True)
@click.option('--data-only', help='open excel in data-only mode, for large file', is_flag=True)
@click.option('--color', help='output with color')
def parse_cli(**kwargs):
    parser = ExcelParser()
    data = parser.parse(kwargs['filename'],
                        data_only=kwargs['data_only'],
                        read_only=kwargs['read_only'],
                        sheet_idx=kwargs['sheet'],
                        choose_one=True,
                        skip=kwargs['skip'],
                        limit=kwargs['limit'])
    parser.export(data,
                  outfile=kwargs['outfile'],
                  fmt=kwargs['outfmt'],
                  indent=kwargs['indent'],
                  sep=kwargs['sep'].encode().decode('unicode_escape'),
                  header=kwargs['header'],
                  index=kwargs['index'],
                  color=kwargs['color'],
                  pager=kwargs['pager'])


if __name__ == '__main__':
    parse_cli()
    