from django.db import models
from student.models import Student
from usercenter.models import UserInfo

# Create your models here.

TYPE_CHOICES = (
    (0, '四人间'),
    (1, '六人间'),
    (2, '八人间'),
)


class DormBuild(models.Model):
    buildname = models.CharField(verbose_name='宿舍楼名称', max_length=50)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    manager = models.ForeignKey(UserInfo, verbose_name='宿舍管理员', null=True, blank=True)


    def __str__(self):
        return self.buildname

    class Meta:
        db_table = 'DormBuild'
        verbose_name = '宿舍楼信息表'
        verbose_name_plural = verbose_name


class DormRoom(models.Model):
    build = models.ForeignKey(DormBuild, verbose_name='所属宿舍楼')
    room_id = models.CharField(verbose_name='宿舍号', max_length=30)
    room_type = models.IntegerField(verbose_name='宿舍类型', choices=TYPE_CHOICES, default=0)
    dorm_head = models.CharField(verbose_name='宿舍长', max_length=20, null=True, blank=True)
    isFull = models.BooleanField(verbose_name='是否满房', default=False)

    def __str__(self):
        return self.build.buildname + "-" + self.room_id

    def get_room_type(self):
        if self.room_type == 0:
            return u"四人间"
        elif self.room_type == 1:
            return u"六人间"
        elif self.room_type == 2:
            return u"八人间"


    class Meta:
        db_table = 'DormRoom'
        verbose_name = '宿舍信息表'
        verbose_name_plural = verbose_name


class BedNumber(models.Model):
    room = models.ForeignKey(DormRoom, verbose_name='所属宿舍')
    bed_num = models.IntegerField(verbose_name='床位号')
    student = models.ForeignKey(Student, verbose_name='学生', null=True, blank=True)

    def __str__(self):
        if self.student == None:
            return self.room.build.buildname + "-" + self.room.room_id + "-" + str(
                self.bed_num) + "-" + "空"
        else:
            return self.room.build.buildname+"-"+self.room.room_id + "-" + str(self.bed_num)+"-"+self.student.studentid+"-"+self.student.name

    class Meta:
        db_table = 'BedNumber'
        verbose_name = '床位信息表'
        verbose_name_plural = verbose_name


class AccessRecords(models.Model):
    student = models.ForeignKey(Student, verbose_name='学生')
    enter_time = models.DateTimeField(verbose_name='进入时间', null=True, blank=True)
    entry_time = models.DateTimeField(verbose_name='出去时间', null=True, blank=True)

    def __str__(self):
        return self.student.name

    class Meta:
        verbose_name = '进出记录表'
        verbose_name_plural = verbose_name


class TemporaryPersonRecords(models.Model):
    student = models.ForeignKey(Student, verbose_name='学生', null=True, blank=True)
    name = models.CharField(verbose_name='姓名', max_length=30)
    mobile = models.CharField(verbose_name='联系电话', max_length=13)
    relation = models.CharField(verbose_name='与学生关系', max_length=20)
    enter_time = models.DateTimeField(verbose_name='进入时间', null=True, blank=True)
    entry_time = models.DateTimeField(verbose_name='出去时间', null=True, blank=True)
    is_carry = models.BooleanField(verbose_name='是否携带人员', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '临时人员登记表'
        verbose_name_plural = verbose_name
