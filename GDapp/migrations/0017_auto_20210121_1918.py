# Generated by Django 3.1.4 on 2021-01-21 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDapp', '0016_auto_20210121_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emimage',
            name='local_file',
            field=models.FilePathField(default='', path='/usr/src/local-images'),
        ),
    ]