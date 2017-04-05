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
        q=None
        if f_data['region']:
            #q = Q(geo__country_code=f_data['region'])
            channels = channels.filter(geo__country_code=f_data['region'])
        channels = channels.annotate(new=F('geo__viewer_percentage')*F('geo__viewer_percentage')).update(view_rate=F('new'))

        for chan in channels:
            print (chan.name, chan.new)
    return render_to_response('filter/filter.html', {
        'form': form,
        'channels': channels
    })

# UPDATE products p
# INNER JOIN categories c ON p.category_id = c.id
# SET p.new_cost = ROUND(p.pleer_cost * (1 + c.price_markup/100), -1)
# WHERE p.update = 1