# Generated by Django 3.1.4 on 2021-04-25 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api', '0015_auto_20210425_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasdaqcomposition',
            name='market_cap',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='nysecomposition',
            name='market_cap',
            field=models.FloatField(null=True),
        ),
    ]
