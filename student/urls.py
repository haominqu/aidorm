from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'editstudent', StudentEdit.as_view(), name='edit_student'),
    url(r'editstutail', StuDetailEdit.as_view(), name='edit_stutail'),
]