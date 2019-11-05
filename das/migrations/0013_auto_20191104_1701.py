# Generated by Django 2.2.6 on 2019-11-04 17:01

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('das', '0012_univercitycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='univercity',
            name='project_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='多个特色输入请用逗号分隔', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='院校特色'),
        ),
    ]