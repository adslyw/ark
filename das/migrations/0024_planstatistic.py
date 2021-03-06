# Generated by Django 2.2.6 on 2019-12-08 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0023_auto_20191203_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ls1', models.IntegerField()),
                ('ls2', models.IntegerField()),
                ('ls3', models.IntegerField()),
                ('lr1', models.IntegerField()),
                ('lr2', models.IntegerField()),
                ('lr3', models.IntegerField()),
                ('as1', models.IntegerField()),
                ('as2', models.IntegerField()),
                ('as3', models.IntegerField()),
                ('ar1', models.IntegerField()),
                ('ar2', models.IntegerField()),
                ('ar3', models.IntegerField()),
                ('hs1', models.IntegerField()),
                ('hs2', models.IntegerField()),
                ('hs3', models.IntegerField()),
                ('hr1', models.IntegerField()),
                ('hr2', models.IntegerField()),
                ('hr3', models.IntegerField()),
                ('admission_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='das.AdmissionYear')),
                ('subject_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='das.SubjectType')),
                ('univercity_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='das.UnivercityCode')),
            ],
            options={
                'verbose_name': 'PlanStatistic',
                'verbose_name_plural': 'PlanStatistics',
            },
        ),
    ]
