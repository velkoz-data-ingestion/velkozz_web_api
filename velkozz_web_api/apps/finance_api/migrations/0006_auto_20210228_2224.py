# Generated by Django 3.1.5 on 2021-02-28 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api', '0005_auto_20210228_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securitypriceohlc',
            name='price_ohlc',
            field=models.FileField(null=True, unique=True, upload_to='finance_api/ohlc'),
        ),
    ]
