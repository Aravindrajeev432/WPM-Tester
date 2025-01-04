from django import template

register = template.Library()

@register.filter
def word_count(text):
    return len(text.split())
