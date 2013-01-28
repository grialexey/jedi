# -*- coding: utf-8 -*-
import re
import pytz
import datetime
import urllib2
from urllib2 import urlopen
from lxml import html, etree
from pyquery import PyQuery as pq
from django.db import IntegrityError
from .models import Ad, Author


def parse(number_of_pages):
    ids = get_themes_ids(number_of_pages)
    for id in ids:
        theme_content = get_theme_content(id)
        save_new_theme(theme_content)


def get_themes_ids(number_of_pages = 1):
    JEDI_BUY_SELL_LINK = "http://jediru.net/viewforum.php?id=16"
    CSS_PATH_TO_THEME_A = "div.tclcon a:first-child"
    UNNEEDED_URL_PART = "viewtopic.php?id="

    themes_ids = []
    for page in range(1, number_of_pages + 1):
        link = JEDI_BUY_SELL_LINK + "&p=" + str(page)
        htmlpage = urlopen(link)
        doc = html.document_fromstring(htmlpage.read())
        for theme_anchor in doc.cssselect(CSS_PATH_TO_THEME_A):
            theme_id = int(theme_anchor.get('href').replace(UNNEEDED_URL_PART, ""))
            themes_ids.append(theme_id)
    return themes_ids


def get_theme_content(theme_id):
    JEDI_THEME_URL = "http://jediru.net/viewtopic.php?id="
    CSS_PATH_TO_THEME_TITLE = ".blockpost:first .postright h3"
    CSS_PATH_TO_THEME_DATETIME = ".blockpost:first h2 span a"
    CSS_PATH_TO_THEME_AUTHOR = ".blockpost:first .postleft strong a"
    CSS_PATH_TO_THEME_MESSAGE = ".postmsg:first p"
    UNNEEDED_PROFILE_URL_PART = "profile.php?id="


    link = JEDI_THEME_URL + str(theme_id)

    d = pq(url=link)
    theme_title = d(CSS_PATH_TO_THEME_TITLE).text()
    added = d(CSS_PATH_TO_THEME_DATETIME).text()
    author_name = d(CSS_PATH_TO_THEME_AUTHOR).text()
    author_id = d(CSS_PATH_TO_THEME_AUTHOR).attr('href')
    message = d(CSS_PATH_TO_THEME_MESSAGE).html()

    theme_id = int(theme_id)
    theme_title = unicode(theme_title)
    added = decode_date(unicode(added))
    author_name = unicode(author_name)
    author_id = int(author_id.replace(UNNEEDED_PROFILE_URL_PART, ""))
    message = unicode(clean_message_urls(message))
    price = get_price(message + theme_title)
    category = get_category(theme_title)
    short_title = get_short_title(theme_title, category)

    theme_content = {
        'theme_id': theme_id,
        'theme_title': theme_title,
        'short_title': short_title,
        'added': added,
        'author_id': author_id,
        'author_name': author_name,
        'message': message,
        'price': price,
        'category': category,
    }

    return theme_content


def decode_date(encoded_date):
    time_pattern = re.compile(r'(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)')
    date_pattern = re.compile(r'(?P<day>\d+)-(?P<month>\d+)-(?P<year>\d+)')

    time_matchobj = time_pattern.search(encoded_date)
    hour = time_matchobj.group('hour')
    minute =  time_matchobj.group('minute')
    second = time_matchobj.group('second')
    time = datetime.time(int(hour), int(minute), int(second))

    if u'Сегодня' in encoded_date:
        date = datetime.date.today()
    elif u'Вчера' in encoded_date:
        date = datetime.date.today() - datetime.timedelta(days=1)
    else:
        date_matchobj = date_pattern.search(encoded_date)
        day = date_matchobj.group('day')
        month = date_matchobj.group('month')
        year = date_matchobj.group('year')
        date = datetime.date(int(year), int(month), int(day))

    date_time = datetime.datetime.combine(date, time)
    moscow_tz = pytz.timezone("Europe/Moscow")
    date_time = moscow_tz.localize(date_time)

    return date_time





def save_new_theme(theme):
    author, created = Author.objects.get_or_create(
        id = theme['author_id'],
        name = theme['author_name'],
    )
    ad = Ad(
        id = theme['theme_id'],
        title = theme['theme_title'],
        short_title = theme['short_title'],
        category = theme['category'],
        price = theme['price'],
        added = theme['added'],
        author = author,
        description = theme['message'],
    )
    try:
        ad.save()
    except IntegrityError:
        pass


def get_price(text):
    price_pattern = re.compile(ur"""
                    (?:		#в этом случае пользователь пишет "цена(стоимость,...) 7500"
						(?:цена|стоимость|хочу|ценник|отдам\sза|прошу|него|районе|всего\sза|цена\sвопроса)
						\s{0,3}
						:?
						\s{0,3}
						(\d+)[,.\s]{0,2}(\d*)	#сама цена
						\s{0,5}
						(т|k|к)?
					)
					|
					(?:     #в этом случае пользователь пишет "7500 руб, 7,5т.р.
						(\d+)[,.\s]{0,2}(\d*)	#сама цена
						\s{0,5}
						(?:(тр|тыс|т\.)|(?:руб|р\.\s))
					)
					""", re.X | re.I | re.M | re.U)


    price_matchobj = price_pattern.search(text)

    price = None

    if price_matchobj is not None:
        if price_matchobj.group(1) > price_matchobj.group(4):
            alpha_price = price_matchobj.group(1)
            thousands = price_matchobj.group(2)
            letter_of_thousands = price_matchobj.group(3)
        else:
            alpha_price = price_matchobj.group(4)
            thousands = price_matchobj.group(5)
            letter_of_thousands = price_matchobj.group(6)

        alpha_price = int(alpha_price)

        if alpha_price == 0:
            return None

        alpha_price = unicode(alpha_price) + u"." + thousands
        alpha_price = float(alpha_price)


        if (int(alpha_price) < 50) and not letter_of_thousands:
            price = alpha_price * 1000
        elif letter_of_thousands or thousands:
            price = alpha_price * 1000
        else:
            price = int(alpha_price)

        if price > 1000000:
            return None

    return price



sell_pattern = re.compile(ur"""
        \{?\[?\(?\s? 			# одна из таких скобок
        (?:продают|продам|прдам|прадам|продаю|продается|продаётся|распродажа|продажа|продастся|изучу\sспрос\sна|изучу\sспрос|в\sпродаже)
        \)?\]?\}?
    """, re.X | re.I | re.M | re.U )

buy_pattern = re.compile(ur"""
        \{?\[?\(? 			# одна из таких скобок
        (?:куплю|купил|хочу|приобрету|хочется|купится|купиться|покупка|нужна|нужен|купицца|нужно)
        \)?\]?}?
    """, re.X | re.I | re.M | re.U )

def get_category(theme_title):
    if sell_pattern.search(theme_title):
        category = Ad.SELL
    elif buy_pattern.search(theme_title):
        category = Ad.BUY
    else:
        category = Ad.OTHER
    return category


def get_short_title(theme_title, category):
    if category == Ad.SELL:
        short_theme_title = sell_pattern.sub("", theme_title)
    elif category == Ad.BUY:
        short_theme_title = buy_pattern.sub("", theme_title)
    else:
        short_theme_title = theme_title
    return short_theme_title




def clean_message_urls(message):
    REGEX_FOR_CLEANING_URLS = ur'\"http://go.jediru.net/\?url=(.*?)\"'
    dirt_url_pattern = re.compile(REGEX_FOR_CLEANING_URLS, re.X | re.I | re.M | re.U)
    message_with_cleaned_urls = re.sub(dirt_url_pattern, unquote_replacement, message)
    return message_with_cleaned_urls

def unquote_replacement(matchobj):
    url = matchobj.group(1)
    unquoted_url = urllib2.unquote(url)
    return u"\"" + unquoted_url + u"\""