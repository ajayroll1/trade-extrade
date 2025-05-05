from django import template

register = template.Library()

@register.filter
def filter_payment_type(payment_methods, payment_type):
    return [pm for pm in payment_methods if pm.payment_type == payment_type]

@register.filter
def filter_status(payment_methods, status):
    return [pm for pm in payment_methods if pm.status == status] 