# Generated by Django 2.2.6 on 2019-11-03 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0006_auto_20191103_0033'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AdmissionBatch',
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='univercity',
            name='total_rank',
            field=models.IntegerField(default=999, verbose_name='综合排名'),
        ),
    ]
