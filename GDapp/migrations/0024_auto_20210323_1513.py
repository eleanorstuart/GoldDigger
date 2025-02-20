# Generated by Django 3.1.4 on 2021-03-23 15:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDapp', '0023_emimage_thresh_sens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emimage',
            name='particle_groups',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
        migrations.AlterField(
            model_name='emimage',
            name='threshold_string',
            field=models.CharField(blank=True, default='1, 60', help_text='Input comma-separated values to serve as the upper and lower boundaries for the area of each particle size.', max_length=200),
        ),
    ]
