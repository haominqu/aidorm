from django.conf.urls import include, url
from .views import *


urlpatterns = [
    url(r'clogin', UserLogin.as_view(),name="clogin"),
    url(r'super/base', SuperBaseView.as_view(), name="super_base"),  # 超级管理员对基础设施管理员管理
    url(r'super/school', SuperSchoolView.as_view(), name="super_school"),  # 超级管理员对学校管理员管理
    url(r'super/dorm', SuperDormView.as_view(), name="super_dorm"),  # 超级管理员对宿舍管理员管理
    url(r'super/guide', SuperGuideView.as_view(), name="super_guide"),  # 超级管理员对导员管理
    url(r'unbound/build', UnboundBuildView.as_view(), name="unbound_build"),  # 超级管理员对导员管理
    url(r'change/password', UserChangePassword.as_view(), name="change_password"),  # 用户修改密码
    url(r'unlock', UnLockView.as_view(), name="unlock"),  # 锁屏
    url(r'show/index', ShowIndexView.as_view(), name="show_index"),  # 首页展示
    url(r'message', MessageNewsView.as_view(), name="message"),  # 通知
    url(r'msgdetail', MessageDetailView.as_view(), name="message_detail"),  # 通知
    url(r'^unusualentry', UnusualEntry.as_view(), name='unusualentry'),  # 长时间未出入

]