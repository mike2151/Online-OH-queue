# Generated by Django 2.1.4 on 2019-01-07 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20190104_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answerer_first_name',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='question',
            name='answerer_last_name',
            field=models.CharField(default='', max_length=32),
        ),
    ]
