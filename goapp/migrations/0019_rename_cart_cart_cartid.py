# Generated by Django 4.0.4 on 2022-06-27 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0018_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cart',
            new_name='cartid',
        ),
    ]
