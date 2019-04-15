from django.db import models

# Create your models here.


class College(models.Model):
    college_name = models.CharField(verbose_name='院系名称', max_length=30)
    college_id = models.CharField(verbose_name='院系编码', max_length=30)
    isDelete = models.BooleanField(verbose_name='是否删除', default=False)

    def __str__(self):
        return self.college_name

    class Meta:
        db_table = 'College'
        verbose_name = '院系信息表'
        verbose_name_plural = verbose_name


class Grade(models.Model):
    grade = models.CharField(verbose_name='年级', max_length=30)
    college = models.ManyToManyField(College, verbose_name='院系')

    def __str__(self):
        return self.grade

    class Meta:
        db_table = 'Grade'
        verbose_name = '年级信息表'
        verbose_name_plural = verbose_name


class Major(models.Model):
    college = models.ForeignKey(College, verbose_name='院系')
    major_name = models.CharField(verbose_name='专业名称', max_length=30)
    major_id = models.CharField(verbose_name='专业编码', max_length=30)
    isDelete = models.BooleanField(verbose_name='是否删除', default=False)

    def __str__(self):
        return self.major_name

    class Meta:
        db_table = 'Major'
        verbose_name = '专业信息表'
        verbose_name_plural = verbose_name