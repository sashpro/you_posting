#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import os, django
import sys
import time
from django.utils import timezone as tz
#from init_db import init_db
from random import choice, shuffle

# from base.forms import OrderForm
# from base.areas import AREAS_TUPLE

from datetime import datetime


def add_channels():
    from filter.models import Youtube
    start = time.clock()
    if Youtube.objects.all().count() < 10:
        NAMES = (u'Саня', u'Сашка', u'Анна', u'Игорь', u'Вася', u'Alex', u'Victor', u'Юра', u'Гадюка', u'Чебурашка')
        amount = 10
        for i in range(amount):
            el = Youtube.objects.create(name=choice(NAMES))
    return time.clock() - start


def add_Geostat():
    from filter.models import YoutubeGeoAnalytics
    from filter.models import Youtube
    table = YoutubeGeoAnalytics.objects
    start = time.clock()
    regions = ['RU', 'UA', 'UK', 'USA', 'BL']
    perc = [10, 25, 15, 30, 20]
    if table.all().count() == 0:
        for chan in Youtube.objects.all():
            shuffle(perc)
            for i, reg in zip(range(0,5), regions):
                table.create(youtube_channel=chan, country_code=reg, viewer_percentage=perc[i])
    return time.clock() - start




def main():
    # init_db()

    print 'Create channels. Time for that ', add_channels()
    print 'Create Geostat. Time for that ', add_Geostat()
    # print 'Create stats ', add_stats()
    # # print 'Create Messages. Time for that ', add_messages(argv[1])
    # print 'Create Deals. Time for that', add_deals()
    # print 'Add report to deals. Time for that', add_deal_stats()
    # print 'Add monitoring to platforms. Time for that', add_monitoring()
    # print 'Add deals to platforms. Time for that', add_deals_executed()
    # print 'Add transaction in wallet. Time for that', add_wallets()
    return


if __name__ == '__main__':
     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_django.settings')
     django.setup()
     main()
