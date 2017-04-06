from django.conf.urls import url
from filter import views

urlpatterns = [
    #url(r'^$', views.index_filter),
    url(r'^get_channels/$', views.filter_channels),
]