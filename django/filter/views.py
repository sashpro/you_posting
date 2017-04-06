# -*- encoding: utf-8
from django.shortcuts import render, render_to_response
from django.db.models import Q, Sum, F, Value
from django.db.models.expressions import RawSQL
from .forms import FilterForm
from .models import *


# Create your views here.

def index_filter(request):
    form = FilterForm(request.GET)
    channels = Youtube.objects.all()
    if form.is_valid():
        f_data = form.cleaned_data

        dic={}
        where = ''
        if f_data['region']:
            where = 'WHERE country_code=\"{}\"'.format(f_data['region'])
        dic['geo'] = "(select F_GEO.youtube_channel_id as id, F_GEO.country_code, sum(F_GEO.viewer_percentage) as SB from \"filter_youtubegeoanalytics\" as F_GEO {} group by \"id\")".format(where)

        where=''
        if f_data['age_group'] or f_data['gender']:
            demogr = []
            if f_data['age_group']:
                demogr.append('age_group=\"'+f_data['age_group']+'\"')
            if f_data['gender']:
                demogr.append('gender=\"' + f_data['gender']+'\"')
            where = 'WHERE '+' AND '.join(demogr)
        dic['demo'] = "(select F_DEMO.youtube_channel_id as id, sum(F_DEMO.viewer_percentage) as SB from \"filter_youtubedemographicsanalytics\" as F_DEMO {} group by \"id\")".format(where)

        where = ''
        if f_data['device']:
            where = 'WHERE device_type=\"{}\"'.format(f_data['device'])
        dic['dev'] ="(select F_DEV.youtube_channel_id as id, sum(F_DEV.viewer_percentage) as SB from \"filter_youtubedeviceanalytics\" as F_DEV {} group by \"id\")".format(where)

        where = ''
        if f_data['os']:
            where = 'WHERE os=\"{}\"'.format(f_data['os'])
        dic['os'] = "(select F_OS.youtube_channel_id as id, sum(F_OS.viewer_percentage) as SB from \"filter_youtubeosanalytics\" as F_OS {} group by \"id\")".format(where)

        q = "WITH geo as "+dic['geo']+", demo as "+dic['demo']+",dev as "+dic['dev']+", os as "+dic['os']+\
            "SELECT DISTINCT FY.id, FY.name, FY.view_rate, (geo.SB * demo.SB * os.SB * dev.SB) as \"new\" "\
            "FROM \"filter_youtube\" FY "\
            "INNER JOIN  geo on FY.id = geo.id " \
            "INNER JOIN demo on FY.id = demo.id "\
            "INNER JOIN dev on FY.id = dev.id "\
            "INNER JOIN os on FY.id = os.id "\
            "GROUP BY FY.id, FY.name, FY.view_rate ORDER BY \"new\" DESC "

        print (channels.query)

    return render_to_response('filter/filter.html', {
        'form': form,
        'channels': channels
    })

# UPDATE products p
# INNER JOIN categories c ON p.category_id = c.id
# SET p.new_cost = ROUND(p.pleer_cost * (1 + c.price_markup/100), -1)
# WHERE p.update = 1


# WITH geo as (select F_GEO.youtube_channel_id as id, F_GEO.country_code, sum(F_GEO.viewer_percentage) as SB from "filter_youtubegeoanalytics" as F_GEO
# where country_code = 'UA' group by id),
# demo as (select F_DEMO.youtube_channel_id as id, sum(F_DEMO.viewer_percentage) as SB from "filter_youtubedemographicsanalytics" as F_DEMO WHERE gender = 'male' AND age_group = '13-17' group by id),
# dev as (select F_DEV.youtube_channel_id as id, sum(F_DEV.viewer_percentage) as SB from "filter_youtubedeviceanalytics" as F_DEV
# WHERE device_type = 'DESKTOP' group by id),
# os as (select F_OS.youtube_channel_id as id, sum(F_OS.viewer_percentage) as SB from
# "filter_youtubeosanalytics" as F_OS WHERE os = 'Linux' group by id)
# -- UPDATE "filter_youtube" \
# -- SET FY.view_rate = (geo.SB * demo.SB * os.SB * dev.SB)
# SELECT DISTINCT FY.id, FY.name, FY.view_rate, (geo.SB * demo.SB * os.SB * dev.SB) as 'new'
# FROM  "filter_youtube" FY
# INNER JOIN geo on FY.id = geo.id
# INNER JOIN demo on FY.id = demo.id
# INNER JOIN dev on FY.id = dev.id
# INNER JOIN os on FY.id = os.id
# GROUP BY FY.id, FY.name, FY.view_rate ORDER BY "new" DESC