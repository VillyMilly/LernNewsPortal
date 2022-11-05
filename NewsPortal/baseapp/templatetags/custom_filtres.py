from django import template
import string

register = template.Library()

CENSORED_WORDS = ['свобода', 'выбор', 'демократия']


@register.filter()
def censor(texts: str) -> str:
    list_text = ''.join(i for i in texts if i not in string.punctuation).lower().split(' ')
    list_of_presence_censored_words = [i for i in list_text if i in CENSORED_WORDS]
    for i in list_of_presence_censored_words:
        texts = texts.replace(i.capitalize(), i[0].upper() + '*' * (len(i) - 1))
        texts = texts.replace(i, i[0] + '*' * (len(i) - 1))

    return texts
