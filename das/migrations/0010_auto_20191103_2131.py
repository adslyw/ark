# Generated by Django 2.2.6 on 2019-11-03 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0009_scoreline'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, unique=True, verbose_name='类型')),
            ],
            options={
                'verbose_name': '学科类型',
                'verbose_name_plural': '学科类型',
            },
        ),
        migrations.AddField(
            model_name='scoreline',
            name='admission_batch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='scorelines', to='das.AdmissionBatch', verbose_name='录取批次'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scoreline',
            name='admission_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scorelines', to='das.AdmissionYear', verbose_name='招生年份'),
        ),
        migrations.AddField(
            model_name='scoreline',
            name='subject_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='scorelines', to='das.SubjectType', verbose_name='学科类型'),
            preserve_default=False,
        ),
    ]
