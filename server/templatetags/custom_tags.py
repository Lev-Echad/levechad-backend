from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_string_add(context, field, new_value):
    get_params = context['request'].GET.copy()
    get_params[field] = new_value
    return get_params.urlencode()
