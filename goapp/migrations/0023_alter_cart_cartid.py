# Generated by Django 4.0.4 on 2022-06-28 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0022_evaluator_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cartid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
