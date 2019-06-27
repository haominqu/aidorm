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


# 学校管理员：crud院系信息；crud专业信息；cru年级信息；批量导入学生基本信息；
# 基础设施管理员：crud楼信息；crud房间信息；管理宿舍管理员；
# 导员：采集学生人脸、指纹；为学生分配宿舍；分配床位；查询学生基本信息；
# 宿舍管理员：开闸机；查询学生进出宿舍记录；查询学生所在房间及床位信息；添加学生违纪行为；查看学生违纪行为；

class UserInfo(AbstractUser):
    role = models.IntegerField(verbose_name="角色", choices=MROLE_CHIOCES, default=4)

    def __str__(self):
        return self.username

    def get_role(self):
        if self.role == 0:
            return u'超级管理员'
        elif self.role == 1:
            return u'学校管理员'
        elif self.role == 2:
            return u'基础设施管理'
        elif self.role == 3:
            return u'导员'
        elif self.role == 4:
            return u'宿舍管理员'


    class Meta:
        db_table = 'UserInfo'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name


class MessageNews(models.Model):
    title = models.CharField(verbose_name='通知标题',max_length=50, default='')
    message = models.TextField(verbose_name='通知信息')
    msg_time = models.DateTimeField(verbose_name='通知时间', auto_now_add=True)
    is_read = models.BooleanField(verbose_name='是否已读', default=False)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    to_user = models.ForeignKey(UserInfo)

    class Meta:
        db_table = 'MessageNews'
        verbose_name = '通知信息表'
        verbose_name_plural = verbose_name



