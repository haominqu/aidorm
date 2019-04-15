from rest_framework import serializers
from .models import *

class StudentListSerializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField('sex_field')

    def sex_field(self, obj):
        return obj.get_sex()

    class Meta:
        model = Student
        fields = ('id', 'studentid', 'name', 'phone')


class StudentDetailSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField('student_field')
    major = serializers.SerializerMethodField('major_field')

    def student_field(self, obj):
        return obj.get_student()

    def major_field(self, obj):
        return obj.get_major()

    class Meta:
        model = StudentDetail
        fields = ('id', 'liaisons', 'liaisons_mobile', 'student', 'major', 'dormitory')
