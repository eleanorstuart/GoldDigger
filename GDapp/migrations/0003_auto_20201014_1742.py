# Generated by Django 3.1.2 on 2020-10-14 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDapp', '0002_delete_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile',
            field=models.FileField(upload_to='Input/'),
        ),
    ]
