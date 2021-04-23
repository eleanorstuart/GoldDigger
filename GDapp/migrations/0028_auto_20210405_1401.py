# Generated by Django 3.1.4 on 2021-04-05 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDapp', '0027_merge_20210405_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emimage',
            name='trained_model',
            field=models.CharField(choices=[('43kGoldDigger', 'GoldDigger for small particles in 43k images'), ('87kGoldDigger', 'General GoldDigger (87k)'), ('032521Experimental', '03/25/2021 Experimental GoldDigger')], default='87kGoldDigger', max_length=100),
        ),
    ]