from django.db import models
from dormitory.models import Room

# Create your models here.

class Student(models.Model):
    studentid = models.CharField(verbose_name='学号', max_length=30)
    name = models.CharField(verbose_name='姓名', max_length=50)
    room = models.ForeignKey(Room, verbose_name='所住房间')

    def __str__(self):
        return self.studentid

    class Meta:
        db_table = 'Student'
        verbose_name = '学生信息表'
        verbose_name_plural = verbose_name