# Generated by Django 3.1.4 on 2021-04-25 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api', '0012_auto_20210425_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nasdaqcomposition',
            name='ipo_year',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
