from django.db import models

# Create your models here.

TYPE_CHOICES = (
    (0, '四人间'),
    (1, '六人间'),
    (2, '八人间'),
)


class DormBuild(models.Model):
    buildname = models.CharField(verbose_name='宿舍楼名称', max_length=50)

    def __str__(self):
        return self.buildname

    class Meta:
        db_table = 'DormBuild'
        verbose_name = '宿舍楼信息表'
        verbose_name_plural = verbose_name


class DormRoom(models.Model):
    build = models.ForeignKey(DormBuild, verbose_name='所属楼')
    room_id = models.CharField(verbose_name='宿舍号', max_length=30)
    room_type = models.IntegerField(verbose_name='宿舍类型', choices=TYPE_CHOICES, default=0)
    over_num = models.IntegerField(verbose_name='剩余可住人数')
    over_bed = models.IntegerField(verbose_name='剩余床号')
    picture = models.ImageField(verbose_name='房态图', upload_to='img/room')
    dorm_head = models.CharField(verbose_name='宿舍长', max_length=20)
    isFull = models.BooleanField(verbose_name='是否满房', default=False)

    def __str__(self):
        return self.roomid

    class Meta:
        db_table = 'DormRoom'
        verbose_name = '宿舍信息表'
        verbose_name_plural = verbose_name