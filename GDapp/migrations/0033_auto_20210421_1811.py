# Generated by Django 3.1.4 on 2021-04-21 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDapp', '0032_auto_20210420_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emimage',
            name='threshold_string',
            field=models.CharField(blank=True, default='1, 60', help_text='Input comma-separated values to serve as the upper and lower boundaries for the area of each particle size.', max_length=200),
        ),
        migrations.AlterField(
            model_name='emimage',
            name='trained_model',
            field=models.CharField(choices=[('43kGoldDigger', 'GoldDigger for small particles in 43k images'), ('87kGoldDigger', 'General GoldDigger (87k)'), ('032521Experimental', '03/25/2021 Experimental GoldDigger')], default='87kGoldDigger', max_length=100),
        ),
    ]