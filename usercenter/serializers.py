from rest_framework import serializers
from .models import *



class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField('role_field')

    def role_field(self, obj):
        return obj.get_role()


    class Meta:
        model = UserInfo
        fields = ('id', 'username', 'role')


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        # model = MessageNews4848108521108520
        model = MessageNews
        fields = ('id', 'title', 'message', 'msg_time', 'is_read')
