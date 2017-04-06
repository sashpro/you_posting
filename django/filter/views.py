from django.shortcuts import render, render_to_response
from django.db.models import Q, Sum, F, Value

from .forms import FilterForm
from .models import *


# Create your views here.

def index_filter(request):
    form = FilterForm(request.GET)
    channels = None
    if form.is_valid():
        f_data = form.cleaned_data
        channels = Youtube.objects.all()
        q=Q()
        # q = q*F('geo__viewer_percentage')
        print(f_data)
        dic={}
        if f_data['region']:
            dic['geo__country_code'] = f_data['region']
            channels = channels.filter(geo__country_code=f_data['region'])
        if f_data['age_group']:
            dic['demographics__age_group'] = f_data['age_group']
            q = q & Q(demographics__age_group=f_data['age_group'])

        if f_data['gender']:
            dic['demographics__gender'] = f_data['gender']
            q = q & Q(demographics__gender=f_data['gender'])
        #channels = channels.filter(q)
        #     channels = channels.filter(demographics__gender=f_data['gender'])
        if f_data['device']:
            dic['device_views__device_type']=f_data['device']
            channels = channels.filter(device_views__device_type=f_data['device'])
        if f_data['os']:
            dic['os_views__os']=f_data['os']
            channels = channels.filter(os_views__os=f_data['os'])
        channels =channels.filter(Q(**dic))

        channels = channels.annotate(new=Sum('demographics__viewer_percentage')# *
                                         # Sum(F('device_views__viewer_percentage')/100.0)*
                                         # Sum(F('os_views__viewer_percentage')/100.0)

                                     ).distinct().order_by('-new')#.update(view_rate=F('new'))
        print(channels.query)
        #channels. 'SELECT DISTINCT "filter_youtube"."id", "filter_youtube"."name", "filter_youtube"."title", "filter_youtube"."view_rate",
        # (CAST(SUM("filter_youtubedemographicsanalytics"."viewer_percentage") AS NUMERIC) + CAST(SUM("filter_youtubegeoanalytics"."viewer_percentage") AS NUMERIC)) AS "new"
        # FROM "filter_youtube" LEFT OUTER JOIN "filter_youtubedemographicsanalytics" ON ("filter_youtube"."id" = "filter_youtubedemographicsanalytics"."youtube_channel_id")
        # LEFT OUTER JOIN "filter_youtubegeoanalytics" ON ("filter_youtube"."id" = "filter_youtubegeoanalytics"."youtube_channel_id") GROUP BY "filter_youtube"."id", "filter_youtube"."name", "filter_youtube"."title", "filter_youtube"."view_rate" ORDER BY "new" DESC'
        # for chan in channels:
        #     print (chan.name, chan.new)
    return render_to_response('filter/filter.html', {
        'form': form,
        'channels': channels
    })

# UPDATE products p
# INNER JOIN categories c ON p.category_id = c.id
# SET p.new_cost = ROUND(p.pleer_cost * (1 + c.price_markup/100), -1)
# WHERE p.update = 1


#SELECT "filter_youtube"."id", "filter_youtube"."name", "filter_youtube"."title", "filter_youtube"."view_rate", ("filter_youtubegeoanalytics"."viewer_percentage" * "filter_youtubedemographicsanalytics"."viewer_percentage") AS "new" FROM "filter_youtube" LEFT OUTER JOIN "filter_youtubegeoanalytics" ON ("filter_youtube"."id" = "filter_youtubegeoanalytics"."youtube_channel_id") LEFT OUTER JOIN "filter_youtubedemographicsanalytics" ON ("filter_youtube"."id" = "filter_youtubedemographicsanalytics"."youtube_channel_id")
