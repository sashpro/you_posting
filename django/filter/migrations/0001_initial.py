# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-05 10:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('title', models.TextField(blank=True, null=True)),
                ('view_rate', models.DecimalField(decimal_places=7, default=0, max_digits=14)),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeDemographicsAnalytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_group', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=10)),
                ('viewer_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('youtube_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demographics', to='filter.Youtube')),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeDeviceAnalytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(max_length=50)),
                ('viewer_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('youtube_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_views', to='filter.Youtube')),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeGeoAnalytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=5)),
                ('viewer_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('youtube_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='geo', to='filter.Youtube')),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeOSAnalytics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os', models.CharField(max_length=50)),
                ('viewer_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('youtube_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os_views', to='filter.Youtube')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='youtubeosanalytics',
            unique_together=set([('youtube_channel', 'os')]),
        ),
        migrations.AlterUniqueTogether(
            name='youtubegeoanalytics',
            unique_together=set([('youtube_channel', 'country_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='youtubedeviceanalytics',
            unique_together=set([('youtube_channel', 'device_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='youtubedemographicsanalytics',
            unique_together=set([('youtube_channel', 'age_group', 'gender')]),
        ),
    ]