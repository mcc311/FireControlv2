# Generated by Django 3.2.5 on 2022-09-28 01:50

from django.db import migrations, models
import problems.models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_auto_20220927_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='timeCost',
            field=models.JSONField(default=problems.models.Problem.default_results),
        ),
    ]