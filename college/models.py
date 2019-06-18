from django.db import models
from usercenter.models import *

# Create your models here.

class College(models.Model):
    college_id = models.CharField(verbose_name='院系编码', max_length=30, unique=True)
    college_name = models.CharField(verbose_name='院系名称', max_length=30)
    isDelete = models.BooleanField(verbose_name='是否删除', default=False)

    def __str__(self):
        return self.college_name

    class Meta:
        db_table = 'College'
        verbose_name = '院系信息表'
        verbose_name_plural = verbose_name


class Major(models.Model):
    college = models.ForeignKey(College, verbose_name='院系')
    major_id = models.CharField(verbose_name='专业编码', max_length=30, unique=True)
    major_name = models.CharField(verbose_name='专业名称', max_length=30)
    isDelete = models.BooleanField(verbose_name='是否删除', default=False)

    def __str__(self):
        return self.college.college_name+"-"+self.major_name

    class Meta:
        db_table = 'Major'
        verbose_name = '专业信息表'
        verbose_name_plural = verbose_name


class Grade(models.Model):
    grade = models.CharField(verbose_name='年级', max_length=30, unique=True)

    def __str__(self):
        return self.grade

    class Meta:
        db_table = 'Grade'
        verbose_name = '年级信息表'
        verbose_name_plural = verbose_name


class ClassInfo(models.Model):
    major = models.ForeignKey(Major, verbose_name='专业')
    grade = models.ForeignKey(Grade, verbose_name='年级')
    class_name = models.CharField(verbose_name='班级', max_length=50)
    class_code = models.CharField(verbose_name='班级编码', max_length=30, unique=True, null=False, blank=False)
    guide = models.ForeignKey(UserInfo, verbose_name='导员')

    def __str__(self):
        return self.grade.grade + self.major.major_name + self.class_name

    class Meta:
        verbose_name = '班级信息表'
        verbose_name_plural = verbose_name


