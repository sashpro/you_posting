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