# Generated by Django 4.0.4 on 2022-06-09 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluator',
            name='password',
        ),
    ]
