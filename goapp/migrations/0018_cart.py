# Generated by Django 4.0.4 on 2022-06-27 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0017_user_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('cart', models.IntegerField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('uprice', models.FloatField()),
                ('tprice', models.FloatField()),
                ('p', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goapp.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goapp.user')),
            ],
        ),
    ]
