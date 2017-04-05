from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Youtube(models.Model):
    name = models.CharField(max_length=255)
    title = models.TextField(blank=True, null=True)
    view_rate = models.DecimalField(default=0, max_digits=14, decimal_places=7)


class YoutubeGeoAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'country_code', ),)

    youtube_channel = models.ForeignKey(Youtube, related_name='geo')
    country_code = models.CharField(max_length=5)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)


class YoutubeDemographicsAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'age_group', 'gender', ),)

    youtube_channel = models.ForeignKey(Youtube, related_name='demographics')
    age_group = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)


class YoutubeDeviceAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'device_type', ),)

    youtube_channel = models.ForeignKey(Youtube, related_name='device_views')
    device_type = models.CharField(max_length=50)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)


class YoutubeOSAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'os', ),)

    youtube_channel = models.ForeignKey(Youtube, related_name='os_views')
    os = models.CharField(max_length=50)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)
