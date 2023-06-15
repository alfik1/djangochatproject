from django import template
import os

register = template.Library()

@register.filter
def get_extension(value):
    print(value,"/*/*")
    print(os.path.splitext(value)[1][0:])
    return os.path.splitext(value)[1][0:]
