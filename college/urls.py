from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^editcollege', CollegeEdit.as_view(), name='edit_college'),
    url(r'^editmajor', MajorEdit.as_view(), name='edit_major'),
 ]