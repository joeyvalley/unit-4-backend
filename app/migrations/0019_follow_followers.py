# Generated by Django 4.2 on 2023-04-07 20:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='followers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]
