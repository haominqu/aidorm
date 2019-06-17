from rest_framework import serializers
from .models import *


class BuildSerializer(serializers.ModelSerializer):

    class Meta:
        model = DormBuild
        fields = ('id', 'buildname')


class BedNumberSerializer(serializers.ModelSerializer):
    build_name = serializers.SerializerMethodField('build_name_field')

    def build_name_field(self, obj):
        return obj.build.buildname

    room_type = serializers.SerializerMethodField('room_type_field')

    def room_type_field(self, obj):
        return obj.get_room_type()

    desc = serializers.SerializerMethodField('desc_field')
    def desc_field(self, obj):
        beds = BedNumber.objects.filter(room=obj)
        bed_info = ""
        for bed in beds:
            bed_num = bed.bed_num
            student_num = bed.student
            if student_num == None:
                student_num = u"空"
                student_name = u"空"
            else:
                student_name = bed.student.name
            student_bed_info = str(bed_num)+"-"+str(student_num)+"-"+str(student_name)
            bed_info = bed_info + student_bed_info + ";"
        return bed_info

    class Meta:
        model = BedNumber
        fields = ("id", "build_name", "room_id", "room_type", "desc")


class AccessRecordSerializer(serializers.ModelSerializer):
    student_code = serializers.SerializerMethodField('student_code_field')

    def student_code_field(self, obj):
        return obj.student.studentid

    student_name = serializers.SerializerMethodField('student_name_field')

    def student_name_field(self, obj):
        return obj.student.name


    class Meta:
        model = AccessRecords
        fields = ('student_code', 'student_name', 'enter_time', 'entry_time')

