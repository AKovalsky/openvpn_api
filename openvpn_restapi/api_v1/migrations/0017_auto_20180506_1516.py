# Generated by Django 2.0.4 on 2018-05-06 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0016_auto_20180504_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='discord_username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
