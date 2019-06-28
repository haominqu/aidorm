from django.contrib import admin
from .models import *
from django.contrib.auth.hashers import make_password

# Register your models here.
class UserInfoAdmin(admin.ModelAdmin):


    def save_model(self, request, obj, form, change):

        obj.password = make_password(obj.password, None, 'pbkdf2_sha1')
        obj.save()



admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(MessageNews)
