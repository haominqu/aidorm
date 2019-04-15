from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
MROLE_CHIOCES = (
    (0, "超级管理员"),
    (1, "学校管理员"),
    (2, "基础设施管理"),
    (3, "导员"),
    (4, "宿舍管理员"),
)

class UserInfo(AbstractUser):
    role = models.IntegerField(verbose_name="角色", choices=MROLE_CHIOCES,default=3)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'UserInfo'
        verbose_name = '宿管信息表'
        verbose_name_plural = verbose_name


