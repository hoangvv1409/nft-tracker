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
