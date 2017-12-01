# -*- coding: utf-8 -*-
"""Format adapter for sql"""

from cli_helpers.utils import filter_dict_by_key
from .preprocessors import (convert_to_string, override_missing_value,
                            style_output)

supported_formats = ('sql-insert','sql-update')

preprocessors = (convert_to_string, )

def escape(d):
    return d.replace('\'', '\\\'')

def adapter(data, headers, table_format=None, preserve_whitespace=False,
            **kwargs):
    if table_format == 'sql-insert':
        h = "`, `".join(headers)
        yield "insert into table (`{}`) values".format(h)
        prefix = "  "
        for d in data:
            values = "', '".join(escape(value) for value in d)
            yield "{}('{}')".format(prefix, values)
            if prefix == "  ":
                prefix = ", "
        yield ";"
    if table_format == 'sql-update':
        for d in data:
            yield "update table set"
            prefix = "  "
            for i, v in enumerate(d[1:]):
                yield "{}`{}` = '{}'".format(prefix, headers[i], escape(v))
                if prefix == "  ":
                    prefix = ", "
            yield "where `{}` = '{}';".format(headers[-1], escape(d[0]))
