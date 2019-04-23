from rest_framework import serializers
from .models import *


class BuildSerializer(serializers.ModelSerializer):

    class Meta:
        model = DormBuild
        fields = ('id', 'buildname')


class RoomSerializer(serializers.ModelSerializer):

    build = BuildSerializer(many=False, read_only=True)

    class Meta:
        model = DormRoom
        fields = ("id", "build", "room_id", "room_type", "over_num", "over_bed", "picture", "dorm_head", "isFull")

