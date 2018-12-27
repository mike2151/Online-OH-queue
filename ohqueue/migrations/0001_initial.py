# Generated by Django 2.1.4 on 2018-12-24 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OHQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('times_open', models.CharField(max_length=1024)),
                ('average_wait_time', models.FloatField(default=0.0)),
                ('questions', models.ManyToManyField(to='questions.Question')),
            ],
        ),
    ]