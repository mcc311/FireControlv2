# Generated by Django 3.2.5 on 2022-09-19 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ships', '0003_auto_20220918_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='defaultWeapons',
            field=models.JSONField(blank=True, default={'weapons': []}),
        ),
    ]
