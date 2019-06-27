from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'edit/student', StudentEdit.as_view(), name='edit_student'),
    url(r'batch/create', BatchCreateView.as_view(), name='batch_create'), # 批量增加学生
    url(r'export/college', ExportCollegeView.as_view(), name='export_college'), # 按院系导出学生
    url(r'export/grade', ExportGradeView.as_view(), name='export_grade'), # 按年级导出学生
    url(r'export/sex', ExportSexView.as_view(), name='export_sex'), # 按性别导出学生
    url(r'bingbuild', Binding_Build.as_view(), name='bing_build'),
    url(r'face/upimage', UploadImageTest.as_view(), name='face_upimage'),
    # url(r'face/batch', Batch_Face.as_view(), name='face_batch'),
]