# Generated by Django 3.1.4 on 2020-12-10 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDapp', '0008_merge_20201210_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emimage',
            name='coordinates6nm',
        ),
        migrations.AddField(
            model_name='emimage',
            name='coordinatesGroup1',
            field=models.FileField(null=True, upload_to='analyzed/coordinatesGroup1'),
        ),
    ]