import json
from django import template

register = template.Library()


@register.filter
def max_value(iterable):
    try:
        return max(iterable)
    except ValueError:
        return None


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def elided_page_range(paginator, number):
    return paginator.get_elided_page_range(number)


@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)


@register.filter
def to_json(value):
    return json.dumps(value)


@register.filter
def pretty_json(value):
    return json.dumps(value, indent=4)
