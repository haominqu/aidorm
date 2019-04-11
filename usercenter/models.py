from django.db import models

# Create your models here.


class HouseMaster(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=30)
    password = models.CharField(verbose_name='密码', max_length=200)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'HouseMaster'
        verbose_name = '宿管信息表'
        verbose_name_plural = verbose_name


