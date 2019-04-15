from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'clogin/', UserLogin.as_view(),name="clogin"),
]