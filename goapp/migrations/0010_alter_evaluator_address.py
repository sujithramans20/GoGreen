# Generated by Django 4.0.4 on 2022-06-19 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0009_alter_evaluator_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluator',
            name='address',
            field=models.CharField(max_length=100),
        ),
    ]
