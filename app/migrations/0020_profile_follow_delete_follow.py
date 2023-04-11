# Generated by Django 4.2 on 2023-04-07 21:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_follow_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follow',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
