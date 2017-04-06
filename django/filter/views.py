# -*- encoding: utf-8
from django.shortcuts import render, render_to_response
from django.db.models import Q, Sum, F, Value
from django.db.models.expressions import RawSQL
from .forms import FilterForm
from .models import *
from rest_framework import viewsets
from filter.serializers import YotubeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def filter_channels(request):
    """
    API endpoint that allows users to be viewed or edited.
    """
    print(request.GET)

    youtube_list = filter(request.GET)  #Youtube.objects.all()
    try:
        new = []
        for lst in youtube_list:
            if lst.id % 2:
                lst.view_rate = int(lst.new) if lst.new is not None else 0
                new.append(lst)
        serializer = YotubeSerializer(new, many=True)
        return Response(serializer.data)
    except (TypeError, AttributeError) as err:
        print ('error ', err.message)
        return Response([])


def filter(params):
    form = FilterForm(params)
    channels = Youtube.objects.all()
    # for par in params:
    #     str
    if form.is_valid():
        f_data = form.cleaned_data
        dic = {}
        where = ''

        if f_data['region']:
            where = 'WHERE country_code=\"{}\"'.format(str(f_data['region']).lower())
        dic['geo'] = "(select F_GEO.youtube_channel_id as geo_id, F_GEO.country_code, CAST(sum(F_GEO.viewer_percentage)as FLOAT) as SB from \"filter_youtubegeoanalytics\" as F_GEO {} group by geo_id)".format(where)

        where=''
        if f_data['age_group'] or f_data['gender']:
            demogr = []
            if f_data['age_group']:
                demogr.append('age_group=\"'+f_data['age_group']+'\"')
            if f_data['gender']:
                demogr.append('gender=\"' + f_data['gender']+'\"')
            where = 'WHERE '+' AND '.join(demogr).lower()
        dic['demo'] = "(select F_DEMO.youtube_channel_id as dem_id, CAST(sum(F_DEMO.viewer_percentage)as FLOAT) as SB from \"filter_youtubedemographicsanalytics\" as F_DEMO {} group by dem_id)".format(where)

        where = ''
        if f_data['device']:
            where = 'WHERE device_type=\"{}\"'.format(str(f_data['device']).lower())
        dic['dev'] ="(select F_DEV.youtube_channel_id as dev_id, CAST(sum(F_DEV.viewer_percentage) as FLOAT) as SB from \"filter_youtubedeviceanalytics\" as F_DEV {} group by dev_id)".format(where)

        where = ''
        if f_data['os']:
            where = 'WHERE os=\"{}\"'.format(unicode(f_data['os']).lower())
        dic['os'] = "(select F_OS.youtube_channel_id as os_id, CAST(sum(F_OS.viewer_percentage) as FLOAT) as SB from \"filter_youtubeosanalytics\" as F_OS {} group by os_id)".format(where)
        # if f_data['view_rate_min'] or f_data['view_rate_max']:
        #     pass
        q = "WITH geo as "+dic['geo']+", demo as "+dic['demo']+",dev as "+dic['dev']+", os as "+dic['os']+\
            "SELECT DISTINCT FY.id, FY.name, FY.view_rate, (geo.SB/100*demo.SB/100*dev.SB/100*os.SB/100)*FY.view_rate as \"new\" "\
            "FROM \"filter_youtube\" FY "\
            "LEFT OUTER  JOIN  geo on FY.id = geo.geo_id " \
            "LEFT OUTER  JOIN demo on FY.id = demo.dem_id "\
            "LEFT OUTER  JOIN dev on FY.id = dev.dev_id "\
            "LEFT OUTER JOIN os on FY.id = os.os_id "\
            "GROUP BY FY.id, FY.name, FY.view_rate ORDER BY \"new\" DESC "
        channels = Youtube.objects.raw(q)


    return channels


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