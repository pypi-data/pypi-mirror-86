"""
Author:     LanHao
Date:       2020/11/16
Python:     python3.6

"""
import logging
from pytz import timezone
from datetime import datetime
from django.conf import settings
from rest_framework import serializers

from .models import Logs, LEVEL_CHOOSE


class TimestampFiled(serializers.Field):

    def to_representation(self, value):
        return value.timestamp()

    def to_internal_value(self, data):
        timestamp = float(data)
        no_tz = datetime.utcfromtimestamp(timestamp)
        return no_tz.astimezone(timezone(settings.TIME_ZONE))


CHOOSE_LEVEL_USE = [each[1] for each in LEVEL_CHOOSE]


class LeveFiled(serializers.Field):
    def to_representation(self, value):
        return LEVEL_CHOOSE[value][1]

    def to_internal_value(self, data):
        return CHOOSE_LEVEL_USE.index(data)


class LogsSerializer(serializers.ModelSerializer):
    created = TimestampFiled()
    levelname = LeveFiled()

    class Meta:
        model = Logs
        fields = "__all__"
