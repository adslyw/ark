from django.db import models

# Create your models here.
class Province(models.Model):

    class Meta:
        verbose_name = "省份"
        verbose_name_plural = "Provinces"

    name = models.CharField(verbose_name='省份名称', max_length=50)

    def __str__(self):
        return self.name


class Rank(models.Model):

    class Meta:
        verbose_name = "综合排名"
        verbose_name_plural = "Ranks"

    name = models.CharField(verbose_name='排名', max_length=50)

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
        verbose_name_plural = "AdmissionBatchs"

    batch_name = models.CharField(verbose_name='批次名称', max_length=50)

    def __str__(self):
        return self.batch_name

class AdmissionYear(models.Model):

    class Meta:
        verbose_name = "招生年份"
        verbose_name_plural = "AdmissionYears"

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

