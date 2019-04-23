from django.db import models
from college.models import *
from dormitory.models import DormRoom

# Create your models here.


SEX_CHOICES = (
    (0, '男'),
    (1, '女'),
)


class Student(models.Model):
    studentid = models.CharField(verbose_name='学号', max_length=30)
    name = models.CharField(verbose_name='姓名', max_length=50)
    sex = models.IntegerField(verbose_name='性别', choices=SEX_CHOICES, default=0)
    phone = models.CharField(verbose_name='联系电话', max_length=13, null=False)
    face = models.CharField(verbose_name='人脸', max_length=50)
    finger = models.CharField(verbose_name='指纹', max_length=50)
    isGraduate = models.BooleanField(verbose_name='是否为毕业生', default=False)

    def __str__(self):
        return self.studentid

    def get_sex(self):
        if self.sex == 0:
            return u'男'
        else:
            return u'女'

    class Meta:
        db_table = 'Student'
        verbose_name = '学生信息表'
        verbose_name_plural = verbose_name


class StudentDetail(models.Model):
    liaisons = models.CharField(verbose_name='紧急联络人', max_length=20)
    liaisons_mobile = models.CharField(verbose_name='紧急联络人电话', max_length=20)
    student = models.OneToOneField(Student, verbose_name='学生信息')
    major = models.ForeignKey(Major, verbose_name='专业信息')
    grade = models.ForeignKey(Grade, verbose_name='年级')
    dormitory = models.ForeignKey(DormRoom, verbose_name='所在宿舍')

    def __str__(self):
        return self.student.studentid

    def get_student(self):
        return self.student.studentid

    def get_major(self):
        return self.major.major_name

    class Meta:
        db_table = 'StudentDetail'
        verbose_name = '学生详细信息表'
        verbose_name_plural = verbose_name

