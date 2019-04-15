from rest_framework import serializers
from .models import *

# class CenterSerializer(serializers.ModelSerializer):
#
#
# 	local = serializers.SerializerMethodField('local_field')
#
# 	def local_field(self, obj):
# 		data = localjson(obj.province, obj.city, obj.area, obj.street)
# 		return data
#
# 	class Meta:
# 		model = Center
# 		fields = ('id','cname', 'ads', 'leader', 'tel', 'local')