# Generated by Django 3.2.9 on 2021-12-06 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20211206_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]
