from enum import Enum
from datetime import datetime
from .dict_ultility import to_dict


def validate_links(url):
    import re

    regex = re.compile(
        r'^https?://'  # http:// or https://
        # flake8: noqa
        # domain
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return url is not None and regex.search(url)


def validate_image_url(url):
    import re

    regex = re.compile(
        r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png|jpeg)')

    return url is not None and regex.search(url)


def first(iterable, default=None):
    for item in iterable:
        return item
    return default


def domain_model_to_orm_schema_mapper(schema, domain_model):
    """
    This only serve generic case (1:1 mapping)
    """
    attrs = [a for a in dir(schema) if not a.startswith('_')]
    orm_obj = schema()
    for attr in attrs:
        if hasattr(domain_model, attr):
            value = getattr(domain_model, attr)
            if isinstance(value, Enum):
                value = value.value
            elif hasattr(value, "__dict__"):
                value = to_dict(value)

            setattr(orm_obj, attr, value)

    return orm_obj


def to_posix(
    value, datetime_str_format='%Y-%m-%dT%H:%M:%S.%f%z',
):
    if isinstance(value, str):
        dt = datetime.strptime(value, datetime_str_format)
    elif isinstance(value, datetime):
        dt = value

    return int(dt.timestamp())
