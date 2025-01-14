# Generated by Django 3.1.4 on 2021-04-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDapp', '0031_auto_20210416_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emimage',
            name='thresh_sens',
            field=models.FloatField(default=4.0),
        ),
        migrations.AlterField(
            model_name='emimage',
            name='threshold_string',
            field=models.CharField(blank=True, default='1, 60', help_text='Input comma-separated values to serve as the lower and upper boundaries for the area of each particle size.', max_length=200),
        ),
    ]
