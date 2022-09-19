# -*- coding: utf-8 -*-

from collections import namedtuple

from cli_helpers.tabular_output import TabularOutputFormatter
from cli_helpers.tabular_output.sql_output_adapter import escape_for_sql_statement, adapter, register_new_formatter

TableReference = namedtuple(
    "TableReference", ["schema", "name", "alias", "is_function"]
)

TableReference.ref = property(
    lambda self: self.alias
                 or (
                     self.name
                     if self.name.islower() or self.name[0] == '"'
                     else '"' + self.name + '"'
                 )
)


def test_escape_for_sql_statement_bytes():
    bts = b"837124ab3e8dc0f"
    escaped_bytes = escape_for_sql_statement(bts)
    assert escaped_bytes == "X'383337313234616233653864633066'"


def test_output_sql_insert():
    global formatter
    formatter = TabularOutputFormatter
    register_new_formatter(formatter)
    data = [
        [
            1,
            "Jackson",
            "jackson_test@gmail.com",
            "132454789",
            "",
            "2022-09-09 19:44:32.712343+08",
            "2022-09-09 19:44:32.712343+08",
        ]
    ]
    header = ["id", "name", "email", "phone", "description", "created_at", "updated_at"]
    table_format = "sql-insert"
    table_refs = (TableReference(schema=None, name='user', alias='"user"', is_function=False),)
    kwargs = {
        "column_types": [int, str, str, str, str, str, str],
        "sep_title": "RECORD {n}",
        "sep_character": "-",
        "sep_length": (1, 25),
        "missing_value": "<null>",
        "integer_format": "",
        "float_format": "",
        "disable_numparse": True,
        "preserve_whitespace": True,
        "max_field_width": 500,
        "tables": table_refs,
    }

    formatter.query = 'SELECT * FROM "user";'
    # For postgresql
    kwargs["delimiter"] = '"'
    output = adapter(data, header, table_format=table_format, **kwargs)
    output_list = [l for l in output]
    expected = [
        'INSERT INTO "user" ("id", "name", "email", "phone", "description", "created_at", "updated_at") VALUES',
        "  ('1', 'Jackson', 'jackson_test@gmail.com', '132454789', '', "
        + "'2022-09-09 19:44:32.712343+08', '2022-09-09 19:44:32.712343+08')",
        ";",
    ]
    assert expected == output_list

    # For mysql
    kwargs["delimiter"] = "`"
    output = adapter(data, header, table_format=table_format, **kwargs)
    output_list = [l for l in output]
    expected = [
        'INSERT INTO `user` (`id`, `name`, `email`, `phone`, `description`, `created_at`, `updated_at`) VALUES',
        "  ('1', 'Jackson', 'jackson_test@gmail.com', '132454789', '', "
        + "'2022-09-09 19:44:32.712343+08', '2022-09-09 19:44:32.712343+08')",
        ";",
    ]
    assert expected == output_list


def test_output_sql_update_pg():
    global formatter
    formatter = TabularOutputFormatter
    register_new_formatter(formatter)
    data = [
        [
            1,
            "Jackson",
            "jackson_test@gmail.com",
            "132454789",
            "",
            "2022-09-09 19:44:32.712343+08",
            "2022-09-09 19:44:32.712343+08",
        ]
    ]
    header = ["id", "name", "email", "phone", "description", "created_at", "updated_at"]
    table_format = "sql-update"
    table_refs = (TableReference(schema=None, name='user', alias='"user"', is_function=False),)
    kwargs = {
        "column_types": [int, str, str, str, str, str, str],
        "sep_title": "RECORD {n}",
        "sep_character": "-",
        "sep_length": (1, 25),
        "missing_value": "<null>",
        "integer_format": "",
        "float_format": "",
        "disable_numparse": True,
        "preserve_whitespace": True,
        "max_field_width": 500,
        "tables": table_refs,
    }
    formatter.query = 'SELECT * FROM "user";'
    # For postgresql
    kwargs["delimiter"] = '"'
    output = adapter(data, header, table_format=table_format, **kwargs)
    output_list = [l for l in output]
    expected = [
        'UPDATE "user" SET',
        '  "name" = \'Jackson\'',
        ', "email" = \'jackson_test@gmail.com\'',
        ', "phone" = \'132454789\'',
        ', "description" = \'\'',
        ', "created_at" = \'2022-09-09 19:44:32.712343+08\'',
        ', "updated_at" = \'2022-09-09 19:44:32.712343+08\'',
        'WHERE "id" = \'1\';']
    assert expected == output_list

    # For mysql
    kwargs["delimiter"] = "`"
    output = adapter(data, header, table_format=table_format, **kwargs)
    output_list = [l for l in output]
    print(output_list)
    expected = [
        'UPDATE `user` SET',
        "  `name` = 'Jackson'",
        ", `email` = 'jackson_test@gmail.com'",
        ", `phone` = '132454789'",
        ", `description` = ''",
        ", `created_at` = '2022-09-09 19:44:32.712343+08'",
        ", `updated_at` = '2022-09-09 19:44:32.712343+08'",
        "WHERE `id` = '1';"]
    assert expected == output_list
