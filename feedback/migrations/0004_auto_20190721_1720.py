# Generated by Django 2.1.4 on 2019-07-21 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20190721_1710'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='help_scale',
            new_name='helpful_scale',
        ),
    ]
