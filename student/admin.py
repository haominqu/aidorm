from django.contrib import admin
from .models import *


# Register your models here.
class StudentFaceShow(admin.ModelAdmin):
    list_display = ("studentid", "name", "sex", "phone", "preview", "finger")
    list_display_links = ('studentid', "name")
    fields = ('studentid', 'name', "sex", "phone", "face", "finger", "isGraduate")
    empty_value_display = "暂无指纹"

    def preview(self, obj):
        return '<img src="/media/%s" height="64" width="64" />' % (obj.face)

    preview.allow_tags = True

    preview.short_description = "人像"

    def finger_not(self, obj):
        return obj.user

    finger_not.empty_value_display = "暂无指纹"







admin.site.register(Student, StudentFaceShow)
admin.site.register(StudentDetail)
