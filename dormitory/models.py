from django.db import models

# Create your models here.

class DormBuild(models.Model):
    buildname = models.CharField(verbose_name='宿舍楼名称', max_length=50)
    username = models.CharField(verbose_name='用户名', max_length=30)
    password = models.CharField(verbose_name='密码', max_length=200)

    def __str__(self):
        return self.buildname

    class Meta:
        db_table = 'DormBuild'
        verbose_name = '宿舍楼信息表'
        verbose_name_plural = verbose_name


class Room(models.Model):
    roomid = models.CharField(verbose_name='宿舍号', max_length=30)
    canlivenum = models.IntegerField(verbose_name='可住人数')
    alrlivenum = models.IntegerField(verbose_name='已住人数')
    unlivenum = models.IntegerField(verbose_name='未住人数')
    build = models.ForeignKey(DormBuild, verbose_name='所属楼')

    def __str__(self):
        return self.roomid

    class Meta:
        db_table = 'Room'
        verbose_name = '房间信息表'
        verbose_name_plural = verbose_name