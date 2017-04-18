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
    """A standard interface to tabular data formatting libraries."""

    _output_formats = {}

    def __init__(self, format_name=None):
        """Set the default *format_name*."""
        self._format_name = format_name

    def set_format_name(self, format_name):
        """Set the TabularOutputFormatter's default format."""
        if format_name in self.supported_formats():
            self._format_name = format_name
        else:
            raise ValueError('unrecognized format_name: {}'.format(
                format_name))

    def get_format_name(self):
        """Get the TabularOutputFormatter's default format."""
        return self._format_name

    def supported_formats(self):
        """Return the supported output format names."""
        return tuple(self._output_formats.keys())

    @classmethod
    def register_new_formatter(cls, format_name, handler, preprocessors=(),
                               kwargs={}):
        """Register a new formatter to format the output."""
        cls._output_formats[format_name] = OutputFormatHandler(
            format_name, preprocessors, handler, kwargs)

    def format_output(self, data, headers, format_name=None, **kwargs):
        """Format the headers and data using a specific formatter.

        *format_name* must be a formatter available in `supported_formats()`.

        All keyword arguments are passed to the specified formatter.

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
