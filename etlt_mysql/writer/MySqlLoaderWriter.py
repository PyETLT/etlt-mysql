import datetime
import os
from abc import ABC
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

import pytz
from etlt.writer.SqlLoaderWriter import SqlLoaderWriter


class MySqlLoaderWriter(SqlLoaderWriter, ABC):
    """
    Writer for storing rows in CSV format optimized for MariaDB and MySQL instances and 'load data local infile'
    statement.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_bool(value: bool, file: Any) -> None:
        """
        Writes a boolean as a field to a CSV file.

        :param value: The boolean.
        :param file: The file like object
        """
        if value:
            file.write('1')
        else:
            file.write('0')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_date(value: datetime.date, file: Any) -> None:
        """
        Writes a date as a field to a CSV file.

        :param value: The date.
        :param file: The file like object
        """
        file.write(value.isoformat())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_datetime(value: datetime.datetime, file: Any) -> None:
        """
        Writes a datetime as a field to a CSV file.

        :param value: The date.
        :param file: The file like object
        """
        zone = value.tzinfo
        if zone and zone != pytz.utc:
            raise ValueError('Only native and UTC timezone supported')
        file.write(value.isoformat())

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_timedelta(value: datetime.timedelta, file: Any) -> None:
        """
        Writes a timedelta as a field to a CSV file.

        :param value: The timedelta.
        :param file: The file like object
        """
        MySqlLoaderWriter.write_string(str(value), file)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_decimal(value: Decimal, file: Any) -> None:
        """
        Writes a decimal as a field to a CSV file.

        :param value: The decimal.
        :param file: The file like object
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_float(value: float, file: Any) -> None:
        """
        Writes a float as a field to a CSV file.

        :param value: The float.
        :param file: The file like object
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_int(value: int, file: Any) -> None:
        """
        Writes an integer as a field to a CSV file.

        :param value: The integer.
        :param file: The file like object
        """
        file.write(str(value))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_none(_, file: Any) -> None:
        """
        Writes None as a field to a CSV file.

        :param _: The None object.
        :param file: The file like object
        """
        file.write('\\N')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_string(value: str, file: Any) -> None:
        """
        Writes a string as a field to a CSV file.

        :param value: The string.
        :param file: The file.
        """
        if value == '':
            file.write('\\N')
        else:
            file.write("'")
            file.write(value.replace('\\', '\\\\').replace("'", "\\'"))
            file.write("'")

    # ------------------------------------------------------------------------------------------------------------------
    def writerow(self, row: Dict[str, Any]) -> None:
        """
        Writes a row to the destination file.

        :param row: The row.
        """
        for field in self._fields:
            self._write_field(row[field])
            self._file.write(',')

        self._file.write(os.linesep)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_uuid(value: UUID, file: Any) -> None:
        """
        Writes a UUID as a field to a CSV file.

        :param value: The UUID.
        :param file: The file like object
        """
        MySqlLoaderWriter.write_string(str(value), file)

    # ------------------------------------------------------------------------------------------------------------------
    def get_bulk_load_sql(self, table_name: str, partition: Optional[str] = None) -> str:
        """
        Returns a SQL statement for bulk loading the data into a table.

        :param table_name: The name of the table.
        :param partition: When applicable, the name of the partition in which the data must be loaded.`
        """
        sql = "load data local infile '{FILENAME}'"
        sql += ' into table `{TABLE_NAME}`'
        if partition is not None:
            sql += ' partition ({PARTITION})'
        sql += ' character set {ENCODING}'
        sql += " fields terminated by ','"
        sql += " optionally enclosed by '\\\''"
        sql += " escaped by '\\\\'"
        sql += " lines terminated by '\\n'"

        return sql.format(FILENAME=self._filename,  # @todo Quoting of filename
                          ENCODING=self._encoding, TABLE_NAME=table_name, PARTITION=partition)


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
