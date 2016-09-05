import datetime
import math
import unittest
from decimal import Decimal
from os import path
from uuid import UUID

import pytz

from etlt_mysql.writer.MySqlLoaderWriter import MySqlLoaderWriter


class MySqlLoaderWriterTest(unittest.TestCase):
    """
    Test cases for MySqlLoaderWriter.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test_types(self):
        filename_actual = path.abspath(path.dirname(__file__)) + '/MySqlLoaderWriterTest/test_types.csv'
        filename_expected = path.abspath(path.dirname(__file__)) + '/MySqlLoaderWriterTest/test_types.expected.csv'

        writer = MySqlLoaderWriter(filename_actual)
        writer.fields = ['bool',
                         'date',
                         'datetime',
                         'timedelta',
                         'decimal',
                         'empty',
                         'float',
                         'int',
                         'none',
                         'str',
                         'uuid']
        rows = [{'bool':      False,
                 'date':      datetime.date(1994, 1, 1),
                 'datetime':  datetime.datetime(1994, 1, 1, 23, 15, 30),
                 'timedelta': datetime.timedelta(days=1, seconds=12345, microseconds=1),
                 'decimal':   Decimal('0.1428571428571428571428571429'),
                 'empty':     '',
                 'float':     1.0 / 3.0,
                 'int':       123,
                 'none':      None,
                 'str':       'Ministry of Silly Walks',
                 'uuid':      UUID('{12345678-1234-5678-1234-567812345678}')},
                {'bool':      True,
                 'date':      None,
                 'datetime':  datetime.datetime(2016, 1, 1, 23, 15, 30, tzinfo=pytz.timezone('UTC')),
                 'timedelta': datetime.timedelta(),
                 'decimal':   Decimal(1) / Decimal(7),
                 'empty':     '',
                 'float':     math.pi,
                 'int':       123,
                 'none':      None,
                 'str':       'мỉאַîśŧґỷ өƒ Šỉŀłỷ שׂǻĺκŝ',  # https://www.tienhuis.nl/utf8-generator
                 'uuid':      UUID(int=0x12345678123456781234567812345678)}]

        with writer:
            for row in rows:
                writer.writerow(row)

        with open(filename_actual, 'rt', encoding='utf8') as file:
            actual = file.read()

        with open(filename_expected, 'rt', encoding='utf8') as file:
            expected = file.read()

        self.assertEqual(actual, expected)

        # ------------------------------------------------------------------------------------------------------------------
        #  @todo test strings with tabs and EOL
        #  @todo test with lading and selecting data from actual MySQL database

# ------------------------------------------------------------------------------------------------------------------
