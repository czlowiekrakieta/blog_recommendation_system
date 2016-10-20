from django import template

register = template.Library()

@register.filter(name='is_even')
def if_even(value):
    print(type(value))
    return not bool(int(value)%2)
