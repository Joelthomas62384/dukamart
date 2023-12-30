from django import template
from math import ceil


register = template.Library()


@register.simple_tag
def progress_bar(total, availables):
    percent = (availables / total) * 100
    return percent


@register.simple_tag
def discount_calculation(price, discount):
    discount_price = int(price) * int(discount)/100
    return ceil(discount_price)
