# Generated by Django 2.1.4 on 2018-12-29 21:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ohqueue', '0005_auto_20181229_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='ohqueue',
            name='last_answer_time',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='ohqueue',
            name='num_questions_answered',
            field=models.IntegerField(default=0),
        ),
    ]
