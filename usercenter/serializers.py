from rest_framework import serializers
from .models import *



class UserSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField('role_field')

    def role_field(self, obj):
        return obj.get_role()


    class Meta:
        model = UserInfo
        fields = ('id', 'username', 'role')

