# Generated by Django 2.0.4 on 2018-05-03 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0009_auto_20180503_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='revoked',
            field=models.BooleanField(default=False),
        ),
    ]
