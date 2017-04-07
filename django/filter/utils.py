from .models import *
from .forms import FilterForm
import sys

def channels_filter(params):
    form = FilterForm(params)
    channels = Youtube.objects.all()
    req = {
        'geo': "(select F_GEO.youtube_channel_id as geo_id, F_GEO.country_code, CAST(sum(F_GEO.viewer_percentage)as FLOAT)"
               " as SB from 'filter_youtubegeoanalytics' as F_GEO {} group by geo_id)",
        'demo': "(select F_DEMO.youtube_channel_id as dem_id, CAST(sum(F_DEMO.viewer_percentage)as FLOAT) as SB "
                "from 'filter_youtubedemographicsanalytics' as F_DEMO {} group by dem_id)",
        'dev': "(select F_DEV.youtube_channel_id as dev_id, CAST(sum(F_DEV.viewer_percentage) as FLOAT) as SB "
               "from 'filter_youtubedeviceanalytics' as F_DEV {} group by dev_id)",
        'os': "(select F_OS.youtube_channel_id as os_id, CAST(sum(F_OS.viewer_percentage) as FLOAT) as SB "
              "from 'filter_youtubeosanalytics' as F_OS {} group by os_id)"
    }
    if form.is_valid():
        f_data = form.cleaned_data
        dic = {}
        where = ''
        if f_data['Country_code']:
            where = 'WHERE country_code=\"{}\"'.format(f_data['Country_code'])
        dic['geo'] = req['geo'].format(where)

        where=''
        if f_data['Age_group'] or f_data['Gender']:
            demogr = []
            if f_data['Age_group']:
                demogr.append('Age_group=\"'+f_data['Age_group']+'\"')
            if f_data['Gender']:
                demogr.append('Gender=\"' + f_data['Gender']+'\"')
            where = 'WHERE '+' AND '.join(demogr)
        dic['demo'] = req['demo'].format(where)

        where = ''
        if f_data['Device_type']:
            where = 'WHERE device_type=\"{}\"'.format(f_data['Device_type'])
        dic['dev'] =req['dev'].format(where)

        where = ''
        if f_data['Os']:
            where = 'WHERE os=\"{}\"'.format(f_data['Os'])
        dic['os'] = req['os'].format(where)

        q = "WITH geo as "+dic['geo']+", demo as "+dic['demo']+",dev as "+dic['dev']+", os as "+dic['os']+\
            "SELECT DISTINCT FY.id, FY.name, FY.view_rate, (geo.SB/100*demo.SB/100*dev.SB/100*os.SB/100)*FY.view_rate as \"new\" "\
            "FROM 'filter_youtube' FY "\
            "INNER JOIN  geo on FY.id = geo.geo_id " \
            "INNER JOIN demo on FY.id = demo.dem_id "\
            "INNER JOIN dev on FY.id = dev.dev_id "\
            "INNER JOIN os on FY.id = os.os_id "\
            "WHERE FY.view_rate BETWEEN {min} AND {max} ".format(min=f_data['View_from'] or 0, max=f_data['View_to'] or sys.maxint)+\
            "GROUP BY FY.id, FY.name, FY.view_rate ORDER BY \"new\" DESC "
        channels = Youtube.objects.raw(q)

    return channels