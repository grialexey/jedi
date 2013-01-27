# -*- coding: utf-8 -*-
from datetime import date, timedelta
from django import template
register = template.Library()

@register.filter('format_date')
def format_date(value):
    today = date.today()
    yesterday = today - timedelta(1)
    if value.date() == today:
        rvalue = u"Сегодня в " + value.strftime("%H:%M")
    elif value.date() == yesterday:
        rvalue = u"Вчера в " + value.strftime("%H:%M")
    else:
        rvalue = value.strftime("%d.%m.%y")
    return rvalue