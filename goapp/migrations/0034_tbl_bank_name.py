# Generated by Django 4.0.4 on 2022-07-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0033_rename_bid_tbl_bank_b_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_bank',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
