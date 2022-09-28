# Generated by Django 3.2.5 on 2022-09-18 16:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weapons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weapon',
            old_name='wid',
            new_name='id',
        ),
        migrations.AddField(
            model_name='weapon',
            name='belongsTo',
            field=models.CharField(choices=[('e', '敵軍'), ('a', '我軍')], default='e', max_length=1),
        ),
        migrations.AddField(
            model_name='weapon',
            name='damage',
            field=models.FloatField(default=0.5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='毀傷值'),
        ),
        migrations.AddField(
            model_name='weapon',
            name='range',
            field=models.FloatField(default=300, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='射程'),
        ),
    ]
