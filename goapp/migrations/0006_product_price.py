# Generated by Django 4.0.4 on 2022-06-16 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0005_adslot_res'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(max_length=30, null=True),
        ),
    ]
