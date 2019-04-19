from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^editbuild', BuildingEdit.as_view(), name='edit_build'),
    url(r'^editroom', RoomEdit.as_view(), name='edit_room'),
 ]