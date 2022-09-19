from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html

register = template.Library()
customer_model = get_user_model()

@register.filter
def address(customer):
    if not isinstance(customer, customer_model):
        return ""
    if customer.address1 and customer.address2:
        address=f"{customer.address1}\n{customer.address2}"
    elif not customer.address2:
        address=f"{customer.address1}"
    return format_html('{}',address)
