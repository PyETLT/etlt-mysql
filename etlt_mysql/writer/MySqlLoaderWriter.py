"""
ETLT-MySQL

Copyright 2016 Set Based IT Consultancy

Licence MIT
"""
import datetime
import os

import pytz
from etlt.writer.SqlLoaderWriter import SqlLoaderWriter


class MySqlLoaderWriter(SqlLoaderWriter):
    """
    Writer for storing rows in CSV format optimized for MariaDB and MySQL instances and 'load data local infile'
    statement.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_bool(value, file):
        """
        Writes a boolean as a field to a CSV file.

        :param bool value: The boolean.
        :param T file: The file.
        """
        if value:
            file.write('1')
        else:
            file.write('0')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_date(value, file):
        """
        Writes a date as a field to a CSV file.

        :param datetime.date value: The date.
        :param T file: The file.
        """
        file.write(value.isoformat())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_datetime(value, file):
        """
        Writes a datetime as a field to a CSV file.

        :param datetime.datetime value: The date.
        :param T file: The file.
        """
        zone = value.tzinfo
        if zone and zone != pytz.utc:
            raise ValueError('Only native and UTC timezone supported')
        file.write(value.isoformat())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_timedelta(value, file):
        """
        Writes a timedelta as a field to a CSV file.

        :param datetime.timedelta value: The timedelta.
        :param T file: The file.
        """
        MySqlLoaderWriter.write_string(str(value), file)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_decimal(value, file):
        """
        Writes a decimal as a field to a CSV file.

        :param decimal.Decimal value: The decimal.
        :param T file: The file.
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_float(value, file):
        """
        Writes a float as a field to a CSV file.

        :param float value: The float.
        :param T file: The file.
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_int(value, file):
        """
        Writes an integer as a field to a CSV file.

        :param int value: The integer.
        :param T file: The file.
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_none(_, file):
        """
        Writes None as a field to a CSV file.

        :param None _: The None object.
        :param T file: The file.
        """
        file.write('\\N')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_string(value, file):
        """
        Writes a string as a field to a CSV file.

        :param str value: The string.
        :param T file: The file.
        """
        if value == '':
            file.write('\\N')
        else:
            file.write("'")
            file.write(value.replace('\\', '\\\\').replace("'", "\\'"))
            file.write("'")

    # ------------------------------------------------------------------------------------------------------------------
    def writerow(self, row):
        """
        Writes a row to the destination file.

        :param dict[str,str|None] row: The row.
        """
        for field in self._fields:
            self._write_field(row[field])
            self._file.write(',')

        self._file.write(os.linesep)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_uuid(value, file):
        """
        Writes a UUID as a field to a CSV file.

        :param uuid.UUID value: The UUID.
        :param T file: The file.
        """
        MySqlLoaderWriter.write_string(str(value), file)

    # ------------------------------------------------------------------------------------------------------------------
    def get_bulk_load_sql(self, table_name):
        """
        Returns a SQL statement for bulk loading the data into a table.

        :param str table_name: The name of the table.

        :rtype: str
        """
        sql = "load data local infile '{FILENAME}'"
        sql += ' into table `{TABLE_NAME}`'
        sql += ' character set {ENCODING}'
        sql += " fields terminated by ','"
        sql += " optionally enclosed by '\\\''"
        sql += " escaped by '\\\\'"
        sql += " lines terminated by '\\n'"

        return sql.format(FILENAME=self._filename,  # @todo Quoting of filename
                          ENCODING=self._encoding,
                          TABLE_NAME=table_name)


# ----------------------------------------------------------------------------------------------------------------------
MySqlLoaderWriter.register_handler("<class 'bool'>", MySqlLoaderWriter.write_bool)
MySqlLoaderWriter.register_handler("<class 'datetime.date'>", MySqlLoaderWriter.write_date)
MySqlLoaderWriter.register_handler("<class 'datetime.datetime'>", MySqlLoaderWriter.write_datetime)
MySqlLoaderWriter.register_handler("<class 'datetime.timedelta'>", MySqlLoaderWriter.write_timedelta)
MySqlLoaderWriter.register_handler("<class 'decimal.Decimal'>", MySqlLoaderWriter.write_decimal)
MySqlLoaderWriter.register_handler("<class 'float'>", MySqlLoaderWriter.write_float)
MySqlLoaderWriter.register_handler("<class 'int'>", MySqlLoaderWriter.write_int)
MySqlLoaderWriter.register_handler("<class 'NoneType'>", MySqlLoaderWriter.write_none)
MySqlLoaderWriter.register_handler("<class 'str'>", MySqlLoaderWriter.write_string)
MySqlLoaderWriter.register_handler("<class 'uuid.UUID'>", MySqlLoaderWriter.write_uuid)
