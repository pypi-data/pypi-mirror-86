import sys
import click

from excelkit.core.concat import ExcelConcat


parse_examples = click.style('''
examples:

    excel-concat input1.xlsx input2.xlsx -o out.xlsx

    excel-concat input1.xlsx input2.xlsx -o out.xlsx --keep-fmt
''', fg='yellow')

@click.command(name='concat', epilog=parse_examples, help=click.style('concat excel files', fg='bright_yellow', bold=True))
@click.argument('infiles', nargs=-1)
@click.option('-o', '--outfile', help='the output filename', default='concat.xlsx')
@click.option('-fmt', '--keep-fmt', help='keep the format, maybe slow for large file', is_flag=True)

def concat_cli(**kwargs):
    concat = ExcelConcat()
    if not kwargs['infiles']:
        concat.logger.info('please input excel files')
        exit()
    concat.logger.info('input {} files: {}'.format(len(kwargs['infiles']), kwargs['infiles']))
    concat.concat(kwargs['infiles'], keep_fmt=kwargs['keep_fmt'])
    concat.save(kwargs['outfile'])
    concat.logger.info('save file: {outfile}'.format(**kwargs))


if __name__ == '__main__':
    concat_cli()
