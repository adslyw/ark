# Generated by Django 2.2.6 on 2019-11-07 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0016_auto_20191107_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='type_name',
        ),
    ]
