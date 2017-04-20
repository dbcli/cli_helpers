# -*- coding: utf-8 -*-
"""A generic tabular data output formatter interface."""

from __future__ import unicode_literals
from collections import namedtuple

from . import (delimited_output_adapter, vertical_table_adapter,
               tabulate_adapter, terminaltables_adapter)

MISSING_VALUE = '<null>'

OutputFormatHandler = namedtuple(
    'OutputFormatHandler',
    'format_name preprocessors formatter formatter_args')


class TabularOutputFormatter(object):
    """An interface to various tabular data formatting libraries.

    The formatting libraries supported include:
      - `tabulate <https://bitbucket.org/astanin/python-tabulate>`_
      - `terminaltables <https://robpol86.github.io/terminaltables/>`_
      - a CLI Helper vertical table layout
      - delimited formats (CSV and TSV)

    :param str format_name: An optional, default format name.

    Usage::

      >>> from cli_helpers.tabular_output import TabularOutputFormatter
      >>> formatter = TabularOutputFormatter(format_name='simple')
      >>> data = ((1, 87), (2, 80), (3, 79))
      >>> headers = ('day', 'temperature')
      >>> print(formatter.format_output(data, headers))
      day    temperature
      -----  -------------
      1      87
      2      80
      3      79

    You can use any :term:`iterable` for the data or headers::

      >>> data = enumerate(('87', '80', '79'), 1)
      >>> print(formatter.format_output(data, headers))
      day    temperature
      -----  -------------
      1      87
      2      80
      3      79

    """

    _output_formats = {}

    def __init__(self, format_name=None):
        """Set the default *format_name*."""
        self._format_name = format_name

    def set_format_name(self, format_name):
        """Set the default format.

        :param str format_name: The display format name.

        """
        if format_name in self.supported_formats():
            self._format_name = format_name
        else:
            raise ValueError('unrecognized format_name: {}'.format(
                format_name))

    def get_format_name(self):
        """Get the current default format.

        :return: The format name.
        :rtype: str or None

        """
        return self._format_name

    def supported_formats(self):
        """Return the names of supported output formats.

        :return: The format names.
        :rtype: tuple

        """
        return tuple(self._output_formats.keys())

    @classmethod
    def register_new_formatter(cls, format_name, handler, preprocessors=(),
                               kwargs={}):
        """Register a new output formatter.

        :param str format_name: The name of the format.
        :param callable handler: The function that formats the data.
        :param tuple preprocessors: The preprocessors to call before
            formatting.
        :param dict kwargs: Keys/values for keyword argument defaults.

        """
        cls._output_formats[format_name] = OutputFormatHandler(
            format_name, preprocessors, handler, kwargs)

    def format_output(self, data, headers, format_name=None, **kwargs):
        """Format the headers and data using a specific formatter.

        *format_name* must be a supported formatter (see
        :meth:`supported_formats`).

        :param iterable data: An :term:`iterable` (e.g. list) of rows.
        :param iterable headers: The column headers.
        :param str format_name: The display format to use (optional, if the
            :class:`TabularOutputFormatter` object has a default format set).
        :param \*\*kwargs: Optional arguments for the formatter.
        :return: The formatted data.
        :rtype: str
        :raises ValueError: If the *format_name* is not recognized.

        """
        format_name = format_name or self._format_name
        if format_name not in self.supported_formats():
            raise ValueError('unrecognized format: {}'.format(format_name))

        (_, preprocessors, formatter,
         fkwargs) = self._output_formats[format_name]
        fkwargs.update(kwargs)
        if preprocessors:
            for f in preprocessors:
                data, headers = f(data, headers, **fkwargs)
        return formatter(data, headers, **fkwargs)


def format_output(data, headers, format_name, **kwargs):
    """Format output using *format_name*.

    This is a wrapper around the :class:`TabularOutputFormatter` class.

    :param iterable data: An :term:`iterable` (e.g. list) of rows.
    :param iterable headers: The column headers.
    :param str format_name: The display format to use.
    :param \*\*kwargs: Optional arguments for the formatter.
    :return: The formatted data.
    :rtype: str

    """
    formatter = TabularOutputFormatter(format_name=format_name)
    return formatter.format_output(data, headers, **kwargs)


for vertical_format in vertical_table_adapter.supported_formats:
    TabularOutputFormatter.register_new_formatter(
        vertical_format, vertical_table_adapter.adapter,
        vertical_table_adapter.preprocessors,
        {'table_format': vertical_format, 'missing_value': MISSING_VALUE})

for delimited_format in delimited_output_adapter.supported_formats:
    TabularOutputFormatter.register_new_formatter(
        delimited_format, delimited_output_adapter.adapter,
        delimited_output_adapter.preprocessors,
        {'table_format': delimited_format, 'missing_value': ''})

for tabulate_format in tabulate_adapter.supported_formats:
    TabularOutputFormatter.register_new_formatter(
        tabulate_format, tabulate_adapter.adapter,
        tabulate_adapter.preprocessors,
        {'table_format': tabulate_format, 'missing_value': MISSING_VALUE})

for terminaltables_format in terminaltables_adapter.supported_formats:
    TabularOutputFormatter.register_new_formatter(
        terminaltables_format, terminaltables_adapter.adapter,
        terminaltables_adapter.preprocessors,
        {'table_format': terminaltables_format, 'missing_value': MISSING_VALUE})
