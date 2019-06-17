from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^index', Index.as_view(), name='index'),
    url(r'^batchinsert', BatchInsert.as_view(), name='batch_insert'),
    url(r'^editcollege', CollegeEdit.as_view(), name='edit_college'),
    url(r'^editmajor', MajorEdit.as_view(), name='edit_major'),
    url(r'^editgrade', GradeEdit.as_view(), name='edit_grade'),
    url(r'^edit/class', ClassInfoView.as_view(), name='edit_class'),  # 班级管理
    # url(r'^savedata', SaveData.as_view(), name='save_data'),

 ]


