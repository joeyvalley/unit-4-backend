# Generated by Django 4.2 on 2023-04-06 18:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_post_dislike_by_profile_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='friend_request',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, null=True, size=None),
        ),
    ]
