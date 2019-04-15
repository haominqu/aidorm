from django.db import models

# Create your models here.
MROLE_CHIOCES = (
    (0, "超级管理员"),
    (1, "学校管理员"),
    (2, "宿舍管理员"),
    (3, "游客")
)

class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=30)
    password = models.CharField(verbose_name='密码', max_length=200)
    role = models.IntegerField(verbose_name="角色", choices=MROLE_CHIOCES,default=3)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'UserInfo'
        verbose_name = '宿管信息表'
        verbose_name_plural = verbose_name


