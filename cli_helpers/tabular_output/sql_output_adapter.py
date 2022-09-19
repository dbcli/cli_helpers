# -*- coding: utf-8 -*-

supported_formats = (
    "sql-insert",
    "sql-update",
    "sql-update-1",
    "sql-update-2",
)

preprocessors = ()


def escape_for_sql_statement(value):
    if isinstance(value, bytes):
        return f"X'{value.hex()}'"
    else:
        return "'{}'".format(value)


def adapter(data, headers, table_format=None, **kwargs):
    """
    This function registers supported_formats to default TabularOutputFormatter

    Parameters:
        data: query result
        headers: columns
        table_format: values from supported_formats
        kwargs:
            tables: tuple parsed from clis. Example: (TableReference(schema=None, name='user', alias='"user"', is_function=False),)
            delimiter: Character surrounds table name or column name when it conflicts with sql keywords.
                       For example, mysql uses ` and postgres uses "
    """
    # tables = extract_tables(formatter.query)
    tables = kwargs.get("tables")
    delimiter = kwargs.get("delimiter")
    if not isinstance(delimiter, str):
        delimiter = '"'

    if tables is not None and len(tables) > 0:
        table = tables[0]
        if table[0]:
            table_name = "{}.{}".format(*table[:2])
        else:
            table_name = table[1]
    else:
        table_name = 'DUAL'.format(delimiter=delimiter)

    header_joiner = '{delimiter}, {delimiter}'.format(delimiter=delimiter)
    if table_format == "sql-insert":
        h = header_joiner.join(headers)
        yield 'INSERT INTO {delimiter}{table_name}{delimiter} ({delimiter}{header}{delimiter}) VALUES'.format(
            table_name=table_name, header=h, delimiter=delimiter)
        prefix = "  "
        for d in data:
            values = ", ".join(escape_for_sql_statement(v) for i, v in enumerate(d))
            yield "{}({})".format(prefix, values)
            if prefix == "  ":
                prefix = ", "
        yield ";"
    if table_format.startswith("sql-update"):
        s = table_format.split("-")
        keys = 1
        if len(s) > 2:
            keys = int(s[-1])
        for d in data:
            yield 'UPDATE {delimiter}{table_name}{delimiter} SET'.format(table_name=table_name, delimiter=delimiter)
            prefix = "  "
            for i, v in enumerate(d[keys:], keys):
                yield '{prefix}{delimiter}{column}{delimiter} = {value}'.format(
                    prefix=prefix, delimiter=delimiter, column=headers[i], value=escape_for_sql_statement(v)
                )
                if prefix == "  ":
                    prefix = ", "
            f = '{delimiter}{column}{delimiter} = {value}'
            where = (
                f.format(delimiter=delimiter, column=headers[i], value=escape_for_sql_statement(d[i]))
                for i in range(keys)
            )
            yield "WHERE {};".format(" AND ".join(where))


def register_new_formatter(TabularOutputFormatter, **kwargs):
    """
    Parameters:
        TabularOutputFormatter: default TabularOutputFormatter imported from cli_helpers
        kwargs: dict required, with key delimiter and tables required.
            For example {"delimiter": "`", "tables": ["table_name"]}
    """
    global formatter
    formatter = TabularOutputFormatter
    for sql_format in supported_formats:
        kwargs["table_format"] = sql_format
        TabularOutputFormatter.register_new_formatter(
            sql_format, adapter, preprocessors, kwargs
        )
