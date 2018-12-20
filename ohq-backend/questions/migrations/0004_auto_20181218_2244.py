# Generated by Django 2.1.4 on 2018-12-18 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20181218_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='author',
        ),
        migrations.AddField(
            model_name='question',
            name='author_email',
            field=models.CharField(default='yo', max_length=512),
            preserve_default=False,
        ),
    ]