from django import template

register = template.Library()

@register.filter
def can_use_coupon(user):
    if user.orders.filter(status='sending').first().payment_type == 'online':
        return True
    return False

@register.filter
def is_payment_type_online(user):
    if user.orders.filter(status='sending').first().payment_type == 'online':
        return True
    return False