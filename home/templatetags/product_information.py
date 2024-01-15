from django import template
from math import ceil


register = template.Library()


@register.simple_tag
def progress_bar(total, availables):
    percent = (availables / total) * 100
    return percent

from math import ceil

@register.simple_tag
def discount_calculation(price, discount):
    discount_price = price * discount/ 100
    # print(discount_price)
    return discount_price 

@register.filter(name='mult')
def mult(value, arg):
    return value * arg


@register.simple_tag
def checkout_price(price,discount,total):
    discount_price = price * discount/ 100
    return round((discount_price * total),2)