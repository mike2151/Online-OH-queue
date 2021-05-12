# Generated by Django 2.1.4 on 2019-07-21 18:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0006_auto_20190721_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='helpful_scale',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]