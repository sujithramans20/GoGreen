# Generated by Django 4.0.4 on 2022-06-21 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0014_alter_evaluator_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adslot',
            name='district',
            field=models.IntegerField(),
        ),
    ]
