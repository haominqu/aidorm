from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(DormBuild)
admin.site.register(DormRoom)
admin.site.register(BedNumber)
admin.site.register(AccessRecords)
admin.site.register(TemporaryPersonRecords)
admin.site.register(FaceMachine)

