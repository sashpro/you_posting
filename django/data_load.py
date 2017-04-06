#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# The above encoding declaration is required and the file must be saved as UTF-8

import os, django
import sys
import time
from django.utils import timezone as tz
#from init_db import init_db
from random import choice, shuffle, randint

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
            el = Youtube.objects.create(name=choice(NAMES), view_rate=randint(50000, 1000000))
    return time.clock() - start


def add_Geostat():
    from filter.models import YoutubeGeoAnalytics
    from filter.models import Youtube
    table = YoutubeGeoAnalytics.objects
    start = time.clock()
    regions = ['ru', 'ua', 'uk', 'usa', 'bl']
    perc = [10, 25, 15, 30, 20]
    if table.all().count() == 0:
        for chan in Youtube.objects.all():
            shuffle(perc)
            for i, reg in zip(range(0,5), regions):
                table.create(youtube_channel=chan, country_code=reg, viewer_percentage=perc[i])
    return time.clock() - start

def add_Devstat():
    from filter.models import YoutubeDeviceAnalytics
    from filter.models import Youtube
    table = YoutubeDeviceAnalytics.objects
    start = time.clock()
    dev = ["desktop","mobile","tablet"]
    perc = [10, 35, 55]
    if table.all().count() == 0:
        for chan in Youtube.objects.all():
            shuffle(perc)
            for i, reg in zip(range(0,5), dev):
                table.create(youtube_channel=chan, device_type=reg, viewer_percentage=perc[i])
    return time.clock() - start

def add_Genderstat():
    from filter.models import YoutubeDemographicsAnalytics
    from filter.models import Youtube
    table = YoutubeDemographicsAnalytics.objects
    start = time.clock()
    age = ['13-17','18-24','25-34', '34-44','45-54','55-64','65+']
    sex = ['male', 'female']
    perc = [5, 15, 10, 25, 20, 18, 7]
    if table.all().count() == 0:
        for chan in Youtube.objects.all():
            shuffle(perc)
            for i, reg in zip(range(0,10), age):
                table.create(youtube_channel=chan, age_group=reg, gender=choice(sex), viewer_percentage=perc[i])
    return time.clock() - start

def add_OSstat():
    from filter.models import YoutubeOSAnalytics
    from filter.models import Youtube
    table = YoutubeOSAnalytics.objects
    start = time.clock()
    os = ['android','windows','linux','mac','ios']
    perc = [17, 23, 10, 20, 30]
    if table.all().count() == 0:
        for chan in Youtube.objects.all():
            shuffle(perc)
            for i, reg in zip(range(0,10), os):
                table.create(youtube_channel=chan, os=reg,  viewer_percentage=perc[i])
    return time.clock() - start



def main():
    # init_db()

    print 'Create channels. Time for that ', add_channels()
    print 'Create Geostat. Time for that ', add_Geostat()
    print 'Create stats DevStat', add_Devstat()
    print 'Create Gender. Time for that ', add_Genderstat()
    print 'Create OS. Time for that', add_OSstat()
    return


if __name__ == '__main__':
     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_django.settings')
     django.setup()
     main()
