from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^index', Index.as_view(), name='index'),
    url(r'^collect/face', CollectFace.as_view(), name='collect_face'),
    url(r'^batch/face', BatchFace.as_view(), name='batch_face'),
    url(r'^batchinsert', BatchInsert.as_view(), name='batch_insert'),
    url(r'^editcollege', CollegeEdit.as_view(), name='edit_college'),
    url(r'^editmajor', MajorEdit.as_view(), name='edit_major'),  # 专业管理
    url(r'^editgrade', GradeEdit.as_view(), name='edit_grade'),
    url(r'^edit/class', ClassInfoView.as_view(), name='edit_class'),  # 班级管理
    url(r'^alread/gradu', AlreadyGraduation.as_view(), name='alread_gradu'),  # 班级毕业
    url(r'^class/detail', ShowClassDetail.as_view(), name='class_detail'),  # 导员查询所管理班级的详细信息
    # url(r'^savedata', SaveData.as_view(), name='save_data'),

 ]


