from django import template

register = template.Library()

CENSORED_WORDS = []

@register.filter()
def censor(text: str) -> str:
    pass