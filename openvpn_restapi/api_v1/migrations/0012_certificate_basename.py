# Generated by Django 2.0.4 on 2018-05-03 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0011_auto_20180503_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='basename',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]