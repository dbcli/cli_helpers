# -*- coding: utf-8 -*-
"""Per-call options must not change another output call's defaults."""

from __future__ import unicode_literals

import pytest

from cli_helpers.tabular_output import format_output, TabularOutputFormatter


@pytest.fixture
def isolated_output_formats(monkeypatch):
    # Do not let either the regression or earlier tests change other tests' options.
    formats = {
        name: handler._replace(formatter_args=handler.formatter_args.copy())
        for name, handler in TabularOutputFormatter._output_formats.items()
    }
    monkeypatch.setattr(TabularOutputFormatter, "_output_formats", formats)


@pytest.mark.parametrize(
    "caller", ["same_instance", "new_instance", "wrapper", "subclass"]
)
@pytest.mark.parametrize(
    "data, override",
    [
        ([[None]], {"missing_value": "one-call-only"}),
        ([["important-data"]], {"max_field_width": 5}),
        ([[1.234567]], {"floatfmt": ".1f"}),
    ],
)
def test_per_call_options_do_not_change_later_output(
    isolated_output_formats, caller, data, override
):
    class InheritedFormatter(TabularOutputFormatter):
        pass

    formatter = TabularOutputFormatter("plain")

    def render(**kwargs):
        if caller == "wrapper":
            result = format_output(data, ["value"], "plain", **kwargs)
        elif caller == "new_instance":
            result = TabularOutputFormatter("plain").format_output(
                data, ["value"], **kwargs
            )
        elif caller == "subclass":
            target = formatter if kwargs else InheritedFormatter("plain")
            result = target.format_output(data, ["value"], **kwargs)
        else:
            result = formatter.format_output(data, ["value"], **kwargs)
        return "\n".join(result)

    original = render()
    assert render(**override) != original
    assert render() == original


def test_per_call_options_preserve_registered_defaults(isolated_output_formats):
    marker = object()
    defaults = {"label": "registered", "marker": marker}
    seen_markers = []

    def render(data, headers, label, marker, **_):
        seen_markers.append(marker)
        return iter([label])

    TabularOutputFormatter.register_new_formatter(
        "call-options", render, kwargs=defaults
    )
    formatter = TabularOutputFormatter("call-options")
    assert list(formatter.format_output([], [], label="temporary")) == ["temporary"]
    assert defaults == {"label": "registered", "marker": marker}
    assert list(formatter.format_output([], [])) == ["registered"]
    assert seen_markers == [marker, marker]


@pytest.mark.parametrize("failure_stage", ["preprocessor", "formatter"])
def test_failed_output_does_not_change_registered_defaults(
    isolated_output_formats, failure_stage
):
    defaults = {"label": "registered"}

    def fail(data, headers, **_):
        raise ValueError("cannot format this input")

    def render(data, headers, label, **_):
        if label == "temporary":
            return fail(data, headers)
        return iter([label])

    TabularOutputFormatter.register_new_formatter(
        "failing-call-options", render, kwargs=defaults
    )
    formatter = TabularOutputFormatter("failing-call-options")
    preprocessors = (fail,) if failure_stage == "preprocessor" else ()
    with pytest.raises(ValueError, match="cannot format this input"):
        formatter.format_output([], [], preprocessors=preprocessors, label="temporary")

    assert defaults == {"label": "registered"}
    assert list(formatter.format_output([], [])) == ["registered"]
