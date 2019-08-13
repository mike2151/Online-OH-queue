# Generated by Django 2.1.4 on 2019-08-13 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190720_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentuser',
            name='most_recent_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='questions.Question', unique=True),
        ),
    ]
