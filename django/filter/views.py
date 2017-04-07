# -*- encoding: utf-8
# from django.shortcuts import render, render_to_response
# from django.db.models import Q, Sum, F, Value
# from django.db.models.expressions import RawSQL
# import sys
# from .forms import FilterForm
# from .models import *
# from rest_framework import viewsets
from .utils import channels_filter
from filter.serializers import YotubeSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def filter_channels(request):
    """
    API endpoint that allows users to be viewed or edited.
    """
    youtube_list = channels_filter(request.GET)  #Youtube.objects.all()
    try:
        new = []
        for lst in youtube_list:
            if lst.id % 2:
                lst.view_rate = int(0 if lst.new is None else lst.new)
                new.append(lst)
        serializer = YotubeSerializer(new, many=True)
        return Response(serializer.data)
    except (TypeError, AttributeError) as err:
        print ('error ', err.message)
        return Response([])

