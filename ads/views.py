# -*- coding: utf-8 -*-
import datetime
import pytz
from django.http import Http404, HttpResponse
from django.views.generic.simple import direct_to_template
from .models import *
import json



def listing_of_ads(request, query=None):
    if request.is_ajax():
        from_date = None

        if "from" in request.GET:
            from_date = request.GET["from"]
            from_date = datetime.datetime.strptime(from_date, u"%Y-%m-%dT%H:%M:%S+00:00")
            utc = pytz.utc
            from_date = utc.localize(from_date)

        json_data = get_ads_json(query, from_date)

        return HttpResponse(json_data, content_type="application/json")
    else:
        bootstrap_json = get_ads_json(query)

        return direct_to_template(request, "ads_listing2.html", { "bootstrap": bootstrap_json, })



def get_ads_json(query=None, from_date=None):
    ADS_TO_LOAD = 32

    ads = Ad.objects.all()
    categorized = False

    if from_date:
        ads = ads.filter(added__lt=from_date)

    if query:
        query = query.strip()
        if u"продажа" in query.lower():
            shorted_query = query.lower().replace(u"продажа", u"").strip()
            ads = ads.filter(category=Ad.SELL, title__icontains=shorted_query)
            categorized = True
        elif u"купят" in query.lower():
            shorted_query = query.lower().replace(u"купят", u"").strip()
            ads = ads.filter(category=Ad.BUY, title__icontains=shorted_query)
            categorized = True
        else:
            ads = ads.filter(title__icontains=query)

    latest_ad = None
    if ads:
        latest_ad = ads.reverse()[0]
    ads = ads[:ADS_TO_LOAD]

    json_data = json.dumps(
        {
            'ads':
                [
                    {
                    'title': o.short_title if categorized else o.title,
                    'id': o.id,
                    'price': o.price,
                    'added': o.added.isoformat(),
                    'description': o.description,
                    } for o in ads
                ],
            'query': query,
            'ended': (latest_ad in ads),
            })

    return json_data