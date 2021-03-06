# Generated by Django 4.0.4 on 2022-07-11 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0038_orderdetails_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='culti',
            fields=[
                ('ct_id', models.AutoField(primary_key=True, serialize=False)),
                ('vname', models.CharField(max_length=30)),
                ('dise', models.CharField(max_length=40)),
                ('sdate', models.DateField()),
                ('ldate', models.DateField()),
                ('status', models.CharField(max_length=40)),
                ('e', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goapp.evaluator')),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goapp.login')),
            ],
        ),
    ]
