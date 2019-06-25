from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    sex = serializers.SerializerMethodField('sex_field')

    def sex_field(self, obj):
        return obj.get_sex()

    student_code = serializers.SerializerMethodField('code_field')
    def code_field(self, obj):
        return obj.studentid

    class Meta:
        model = Student
        fields = ('student_code', 'name', 'sex', 'phone')


class StudentDetailSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)

    major = serializers.SerializerMethodField('major_field')
    def major_field(self, obj):
        return obj.get_major()

    college = serializers.SerializerMethodField('college_field')
    def college_field(self, obj):
        return obj.get_college()

    grade = serializers.SerializerMethodField('grade_field')
    def grade_field(self, obj):
        return obj.get_grade()

    class_info = serializers.SerializerMethodField('class_info_field')
    def class_info_field(self, obj):
        return obj.get_class_info()

    class Meta:
        model = StudentDetail
        fields = ('student', 'liaisons', 'liaisons_mobile', 'college', 'major', 'grade', 'class_info')

