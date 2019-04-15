from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'studentedit/', StudentEdit.as_view(), name='student_edit'),
]