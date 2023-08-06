import os
import sys
import click


from excelkit.core.parse import parse_text
from excelkit.core.build import ExcelBuilder
from excelkit.util.styles import HEAD_STYLES, BODY_STYLES


build_examples = click.style('''
examples:

    excel-build demo/genelist demo/hsa00010.conf

    excel-build demo/genelist demo/hsa00010.conf -o kegg.xlsx

    excel-build demo/genelist demo/hsa00010.conf -o kegg.xlsx -s GENE,KEGG

    excel-build demo/genelist demo/hsa00010.conf -h

    excel-build demo/genelist demo/hsa00010.conf -hs

    excel-build demo/genelist demo/hsa00010.conf -hs -bs

    cat demo/genelist | excel-build
''', fg='yellow')

@click.command(name='build', epilog=build_examples, help=click.style('build excel file', fg='green', bold=True))
@click.argument('filenames', nargs=-1)
@click.option('-sep', '--separator', help='the separator of input files', default='\t')
@click.option('-o', '--outfile', help='the output filename', default='out.xlsx', show_default=True)
@click.option('-s', '--sheetnames', help='the sheetname to output for each file')
@click.option('-h', '--header', help='input files with header', is_flag=True)
@click.option('-af', '--auto-filter', help='auto filter for the header', is_flag=True)

@click.option('-freeze', '--freeze-panes', help='freeze panes, eg. A2 for first row, B1 for first column, B2 for first row and first column')

@click.option('-hs', '--header-style', help='set style for header', type=click.Choice(HEAD_STYLES.keys()))
@click.option('-rc', '--row-colors', help='colors for rows, eg. cyan_green|white_grey, or FF0000,00FF00,0000FF')
def build_cli(**kwargs):
    sheetnames = kwargs['sheetnames'].split(',') if kwargs['sheetnames'] else None
    if kwargs['filenames']:
        files = [open(f) for f in kwargs['filenames']]
    elif not sys.stdin.isatty():
        files = [sys.stdin]
    else:
        exit('please supply one or more files, or stdin')

    if (not sheetnames) or (len(sheetnames) != len(files)):
        sheetnames = [None] * len(files)

    header_style = HEAD_STYLES.get(kwargs['header_style'], {})
    color_list = BODY_STYLES.get(kwargs['row_colors'])
    if kwargs['row_colors'] and not color_list:
        color_list = kwargs['row_colors'].split(',')

    builder = ExcelBuilder()

    for sheetname, f in zip(sheetnames, files):
        if sys.stdin.isatty():
            sheetname = sheetname or os.path.basename(f.name)
        builder.create_sheet(sheetname)
        data = list(parse_text(f, sep=kwargs['separator']))

        if kwargs['header']:
            builder.add_title(data[0], **header_style)
            data = data[1:]

        builder.add_rows(data, color_list=color_list)

        if kwargs['auto_filter']:
            builder.auto_filter()

        if kwargs['freeze_panes']:
            builder.freeze_panes(coordinate=kwargs['freeze_panes'])
        
    builder.save(kwargs['outfile'])


if __name__ == '__main__':
    build_cli()
    