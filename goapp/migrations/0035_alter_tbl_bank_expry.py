# Generated by Django 4.0.4 on 2022-07-03 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0034_tbl_bank_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_bank',
            name='expry',
            field=models.CharField(max_length=6),
        ),
    ]