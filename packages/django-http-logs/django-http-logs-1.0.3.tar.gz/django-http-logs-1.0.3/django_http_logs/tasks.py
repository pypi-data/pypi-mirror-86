"""
Author:     LanHao
Date:       2020/11/16
Python:     python3.6

"""

from celery import shared_task

from .serializers import LogsSerializer

@shared_task
def add_log(data):
    serializer = LogsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
