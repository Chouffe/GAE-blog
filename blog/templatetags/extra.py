from django import template

register = template.Library()


@register.filter
def get_id(instance):
    return instance.key().id()
