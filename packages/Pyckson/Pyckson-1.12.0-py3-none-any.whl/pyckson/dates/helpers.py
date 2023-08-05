from pyckson.const import PYCKSON_DATE_FORMATTER, PYCKSON_EXPLICIT_NULLS, has_cls_attr, get_cls_attr
from pyckson.dates.model import DateFormatter
from pyckson.dates.raw_formatter import RawDateFormatter

global_date_formatter = RawDateFormatter()
global_explicit_nulls = False


def configure_date_formatter(formatter: DateFormatter):
    global global_date_formatter
    global_date_formatter = formatter


def get_date_formatter() -> DateFormatter:
    return global_date_formatter


def get_class_date_formatter(cls) -> DateFormatter:
    if has_cls_attr(cls, PYCKSON_DATE_FORMATTER):
        return get_cls_attr(cls, PYCKSON_DATE_FORMATTER)
    else:
        return get_date_formatter()


def configure_explicit_nulls(use_explicit_nulls: bool):
    global global_explicit_nulls
    global_explicit_nulls = use_explicit_nulls


def get_use_explicit_nulls() -> bool:
    return global_explicit_nulls


def get_class_use_explicit_nulls(cls) -> bool:
    if has_cls_attr(cls, PYCKSON_EXPLICIT_NULLS):
        return get_cls_attr(cls, PYCKSON_EXPLICIT_NULLS)
    else:
        return get_use_explicit_nulls()
