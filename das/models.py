# -*- coding: utf-8 -*-
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedProvince(TaggedItemBase):
    content_object = models.ForeignKey(
        'Province',
        on_delete=models.CASCADE,
    )

class Province(models.Model):

    class Meta:
        verbose_name = "省份"
        verbose_name_plural = "省份"

    name = models.CharField(verbose_name='省份名称', max_length=50)
    tags = TaggableManager(verbose_name='标签', blank=True, through=TaggedProvince)

    def __str__(self):
        return self.name

class City(models.Model):

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = "城市"

    name = models.CharField(verbose_name='城市', max_length=50, unique=True)
    province = models.ForeignKey(
        Province,
        related_name='cities',
        on_delete=models.CASCADE,
        verbose_name='省份',
    )
    tags = TaggableManager(verbose_name='标签', blank=True)

    def __str__(self):
        return self.name


class Rank(models.Model):

    class Meta:
        verbose_name = "学科档次"
        verbose_name_plural = "学科档次"

    name = models.CharField(verbose_name='档次', max_length=50)

    def __str__(self):
        return self.name


class ExamDivision(models.Model):

    class Meta:
        verbose_name = "高考分科"
        verbose_name_plural = "ExamDivisions"

    subject = models.CharField(verbose_name='科目', max_length=50)

    def __str__(self):
        return self.subject

class AdmissionBatch(models.Model):

    class Meta:
        verbose_name = "录取批次"
        verbose_name_plural = "录取批次"

    batch_name = models.CharField(verbose_name='批次名称', max_length=100, unique=True)

    def __str__(self):
        return self.batch_name

class AdmissionYear(models.Model):

    class Meta:
        verbose_name = "招生年份"
        verbose_name_plural = "招生年份"

    year = models.CharField(verbose_name='年份', max_length=50)

    def __str__(self):
        return self.year

class SchoolType(models.Model):

    class Meta:
        verbose_name = "高校类型"
        verbose_name_plural = "SchoolTypes"

    type_name = models.CharField(verbose_name='类型', max_length=50)

    def __str__(self):
        return self.type_name

class SchoolFeature(models.Model):

    class Meta:
        verbose_name = "院校特色"
        verbose_name_plural = "SchoolFeatures"

    feature = models.CharField(verbose_name='特色', max_length=50)
    def __str__(self):
        return self.feature

class Affiliation(models.Model):

    class Meta:
        verbose_name = "隶属关系"
        verbose_name_plural = "Affiliations"

    belong_to = models.CharField(verbose_name='隶属于', max_length=50)

    def __str__(self):
        return self.belong_to

class SchoolLevel(models.Model):

    class Meta:
        verbose_name = "高校性质"
        verbose_name_plural = "SchoolLevels"

    level = models.CharField(verbose_name='高校性质', max_length=50)

    def __str__(self):
        return self.level


class School(models.Model):

    class Meta:
        verbose_name = "院校"
        verbose_name_plural = "Schools"

    name = models.CharField(verbose_name='院校名称', max_length=50)
    is_key_universities = models.BooleanField(
        verbose_name='是否重点院校',
        default=False
    )
    home_page = models.CharField(verbose_name='院校主页', max_length=255, null=True, blank=True)
    features = models.CharField(verbose_name='院校特色', max_length=255, null=True, blank=True)

    province = models.ForeignKey(
        Province,
        related_name='schools',
        on_delete=models.CASCADE
    )
    rank = models.ForeignKey(
        Rank,
        related_name='schools',
        on_delete=models.CASCADE
    )
    level = models.ForeignKey(
        SchoolLevel,
        related_name='schools',
        on_delete=models.CASCADE
    )
    affiliation = models.ForeignKey(
        Affiliation,
        related_name='schools',
        on_delete=models.CASCADE
    )
    school_type = models.ForeignKey(
        SchoolType,
        related_name='schools',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return self.name

class Univercity(models.Model):

    class Meta:
        verbose_name = "院校信息"
        verbose_name_plural = "院校信息"

    name = models.CharField(verbose_name='院校名称', max_length=255)
    total_rank = models.IntegerField(verbose_name='综合排名', default=999)
    project_tags = TaggableManager(verbose_name='院校特色', blank=True, help_text='多个特色输入请用逗号分隔')
    is_private = models.BooleanField(verbose_name='是否民办院校', default=False)

    city = models.ForeignKey(
        City,
        related_name='univercities',
        on_delete=models.CASCADE,
        verbose_name='所在城市',
        null=True,
    )

    def __str__(self):
        return self.name


class SubjectType(models.Model):

    class Meta:
        verbose_name = "考生类型"
        verbose_name_plural = "考生类型"

    type_name = models.CharField(verbose_name='类型', max_length=50, unique=True)
    def __str__(self):
        return self.type_name



class Subject(models.Model):

    class Meta:
        verbose_name = "学科门类"
        verbose_name_plural = "学科门类"

    name = models.CharField(verbose_name='专业', max_length=255)
    subject_type = models.ForeignKey(
        SubjectType,
        related_name='subjects',
        on_delete=models.CASCADE,
        verbose_name='考生类型',
        null=True,
    )

    def __str__(self):
        return self.name

class ScoreLine(models.Model):

    class Meta:
        verbose_name = "历年分数线"
        verbose_name_plural = "历年分数线"
        unique_together = [['subject_type', 'admission_batch', 'admission_year']]

    score = models.IntegerField(verbose_name='分数')
    subject_type = models.ForeignKey(
        SubjectType,
        related_name='scorelines',
        on_delete=models.CASCADE,
        verbose_name='学科类型'
    )
    admission_batch = models.ForeignKey(
        AdmissionBatch,
        related_name='scorelines',
        on_delete=models.CASCADE,
        verbose_name='录取批次'
    )
    admission_year = models.ForeignKey(
        AdmissionYear,
        related_name='scorelines',
        on_delete=models.CASCADE,
        verbose_name='招生年份',
    )

    def __str__(self):
        return str(self.score)

class UnivercityCode(models.Model):

    class Meta:
        verbose_name = "院校代码"
        verbose_name_plural = "院校代码"

    code = models.CharField(verbose_name='代码', max_length=50, unique=True)
    univercity_name_alias = models.CharField(verbose_name='学校名称(含招生条件备注)', max_length=255)
    page1 = models.CharField(verbose_name='挑大学选专业书页码', max_length=50, blank=True, default='')
    page2 = models.CharField(verbose_name='汇编书页码', max_length=50, blank=True, default='')
    univercity = models.ForeignKey(
        Univercity,
        related_name='univercity_codes',
        on_delete=models.CASCADE,
        verbose_name='高校',
        null=True,
    )

    def __str__(self):
        return self.code

class Plan(models.Model):

    class Meta:
        verbose_name = "历年招生数据"
        verbose_name_plural = "历年招生数据"

    univercity_code = models.ForeignKey(
        UnivercityCode,
        related_name='plans',
        on_delete=models.CASCADE,
        verbose_name='院校代码'
    )
    subject_type = models.ForeignKey(
        SubjectType,
        related_name='plans',
        on_delete=models.CASCADE,
        verbose_name='考生类型',
    )
    admission_batch = models.ForeignKey(
        AdmissionBatch,
        related_name='plans',
        on_delete=models.CASCADE,
        verbose_name='录取批次',
    )
    admission_year = models.ForeignKey(
        AdmissionYear,
        related_name='plans',
        on_delete=models.CASCADE,
        verbose_name='录取年份',
    )
    plan_amount = models.IntegerField(verbose_name='计划数', default=0)
    actual_amount = models.IntegerField(verbose_name='实录数', default=0)
    highest_score = models.IntegerField(verbose_name='最高分', default=0)
    highest_rank = models.IntegerField(verbose_name='最高位次', default=0)
    lowest_score = models.IntegerField(verbose_name='最低分', default=0)
    lowest_rank = models.IntegerField(verbose_name='最低位次', default=0)
    average_score = models.IntegerField(verbose_name='平均分', default=0)
    average_rank = models.IntegerField(verbose_name='平均位次', default=0)

    @property
    def score_line(self):
        if self.admission_batch.batch_name == '本科二批':
            batch_name = '本科二批'
        else:
            batch_name = '本科一批'

        score_line = ScoreLine.objects.get(
            admission_batch__batch_name=batch_name,
            subject_type=self.subject_type,
            admission_year=self.admission_year,
        )

        return score_line

    @property
    def highest_score_diff(self):
        return self.highest_score - self.score_line.score

    @property
    def lowest_score_diff(self):
        return self.lowest_score - self.score_line.score

    @property
    def average_score_diff(self):
        return self.average_score - self.score_line.score

    def __str__(self):
        return str(self.plan_amount)

class ScoreStatistic(models.Model):

    class Meta:
        verbose_name = "考生成绩统计表"
        verbose_name_plural = "考生成绩统计表"

    score = models.IntegerField(verbose_name='分数')
    number = models.IntegerField(verbose_name='人数')
    cumulative_number = models.IntegerField(verbose_name='累计人数')
    admission_year = models.ForeignKey(
        AdmissionYear,
        related_name='score_statistics',
        on_delete=models.CASCADE,
        verbose_name='高考年份',
    )
    subject_type = models.ForeignKey(
        SubjectType,
        related_name='score_statistics',
        on_delete=models.CASCADE,
        verbose_name='考生类型',
    )

    def __str__(self):
        return self.score

class PlanStatistic(models.Model):

    class Meta:
        verbose_name = "PlanStatistic"
        verbose_name_plural = "PlanStatistics"

    ls1 = models.IntegerField(default=0)
    ls2 = models.IntegerField(default=0)
    ls3 = models.IntegerField(default=0)
    lr1 = models.IntegerField(default=0)
    lr2 = models.IntegerField(default=0)
    lr3 = models.IntegerField(default=0)
    as1 = models.IntegerField(default=0)
    as2 = models.IntegerField(default=0)
    as3 = models.IntegerField(default=0)
    ar1 = models.IntegerField(default=0)
    ar2 = models.IntegerField(default=0)
    ar3 = models.IntegerField(default=0)
    hs1 = models.IntegerField(default=0)
    hs2 = models.IntegerField(default=0)
    hs3 = models.IntegerField(default=0)
    hr1 = models.IntegerField(default=0)
    hr2 = models.IntegerField(default=0)
    hr3 = models.IntegerField(default=0)

    d1 = models.IntegerField(default=0)
    d2 = models.IntegerField(default=0)
    d3 = models.IntegerField(default=0)
    d4 = models.IntegerField(default=0)
    d5 = models.IntegerField(default=0)
    d6 = models.IntegerField(default=0)
    d7 = models.IntegerField(default=0)

    univercity_code = models.ForeignKey(
        UnivercityCode,
        on_delete=models.CASCADE,
    )
    admission_year = models.ForeignKey(
        AdmissionYear,
        on_delete=models.CASCADE,
    )
    subject_type = models.ForeignKey(
        SubjectType,
        on_delete=models.CASCADE,
    )
    admission_batch = models.ForeignKey(
        AdmissionBatch,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return ''
