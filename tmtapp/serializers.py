from rest_framework import serializers
from .models import *


class FileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=100000000000, allow_empty_file=False, use_url=True)


class BugSerializer(serializers.ModelSerializer):
    # create_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    class Meta:
        model = Bugs
        exclude = ('bug_info',)


class AppFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=100000000000, allow_empty_file=False, use_url=True)
    constraint = serializers.BooleanField(default=True, label='是否强制更新')

    class Meta:
        model = AppUpdate
        exclude = ('status', 'md5', 'file_url', 'file_path', 'file_size')

class AppHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUpdate
        # exclude = ('status', 'md5', 'file_url', 'file_path', 'file_size')
        fields='__all__'
