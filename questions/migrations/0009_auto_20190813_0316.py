# Generated by Django 2.1.4 on 2019-08-13 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20190720_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='feedback_for_q',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='feedback.Feedback', unique=True),
        ),
    ]
