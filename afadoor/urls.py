from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^getfacelist', GetFaceList.as_view(), name='get_facelist'),
    # url(r'^editroom', RoomEdit.as_view(), name='edit_room'),
    # url(r'^editbed', BedEdit.as_view(), name='edit_bed'),
    # url(r'^enter/record', EnterRecordView.as_view(), name='enter_record'),  # 进入宿舍记录
    # url(r'^entry/record', EntryRecordView.as_view(), name='entry_record'),  # 出入宿舍记录
    # url(r'^enter/temporary', TemportaryPersonEnter.as_view(), name='enter_temporary'),  # 临时人员进入宿舍记录
    # url(r'^entry/temporary', TemportaryPersonEntry.as_view(), name='entry_temporary'),  # 临时人员出入宿舍记录
    # url(r'^enter/carry', CarryPersonEnter.as_view(), name='enter_carry'),  # 携带临时人员进入宿舍记录
    # url(r'^entry/carry', CarryPersonEntry.as_view(), name='entry_carry'),  # 携带临时人员出入宿舍记录
    # url(r'^export/access', ExportAccessView.as_view(), name='export_access'),  # 出入记录
    # url(r'^long/enter', LongTimeEnter.as_view(), name='long_enter'),  # 长时间未进入
    # url(r'^long/entry', LongTimeEntry.as_view(), name='long_entry'),  # 长时间未出入
 ]