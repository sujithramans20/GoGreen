# Generated by Django 4.0.4 on 2022-07-11 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0039_culti'),
    ]

    operations = [
        migrations.AddField(
            model_name='culti',
            name='slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goapp.adslot'),
        ),
    ]
