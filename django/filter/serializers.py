from .models import Youtube
from rest_framework import serializers


class YotubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtube
        fields = ('id', 'name', 'title', 'view_rate')