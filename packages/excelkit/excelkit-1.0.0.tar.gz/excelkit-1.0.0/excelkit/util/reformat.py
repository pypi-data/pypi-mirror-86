"""
    reformat rows data from excel

    available format:
        - prettytable
        - json
        - tsv
"""
import json
from collections import Counter

import click
import openpyxl
import prettytable

from simple_loggers import SimpleLogger


class Formatter(object):
    logger = SimpleLogger('DataFormatter')
    def __init__(self, rows, header=True):
        self.rows = rows
        self.header = header and self.check_header()

    def check_header(self):
        counter = Counter(self.rows[0])
        dup_names = [k for k, v in counter.items() if v > 1]
        if dup_names:
            click.secho('could not set header=True as duplicate field names: {}'.format(dup_names),
                        err=True, fg='yellow')
            return False
        return True

    def to_table(self, align='l', index=False):
        """
            return a prettytable object

            >>> t = to_table()
            >>> str(t)
            >>> t.get_string()
            >>> t.get_html_string()
        """
        table = prettytable.PrettyTable()
        if self.header:
            field_names = self.rows[0]
            rows = self.rows[1:]
        else:
            field_names = list(map(
                openpyxl.utils.get_column_letter,
                range(1, len(self.rows[0]) + 1)
            ))
            rows = self.rows

        if index:
            table.field_names = ['Index'] + field_names
        else:
            table.field_names = field_names

        for n, row in enumerate(rows, 1):
            if index:
                row = [n] + row
            table.add_row(row)

        for field in table.field_names:
            table.align[field] = align

        return table
        
    def to_json(self, indent=None, ensure_ascii=False):
        data = []
        if not self.header:
            data = self.rows
        else:
            fields = self.rows[0]
            rows = self.rows[1:]
            for row in rows:
                context = dict(zip(fields, row))
                data.append(context)
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

    def to_tsv(self, sep='\t', quote=''):
        data = []
        for row in self.rows:
            line = sep.join('{0}{1}{0}'.format(quote, each) for each in row)
            data.append(line)
        return '\n'.join(data)
