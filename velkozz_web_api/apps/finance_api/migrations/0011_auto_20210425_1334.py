# Generated by Django 3.1.4 on 2021-04-25 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api', '0010_auto_20210425_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nysecomposition',
            name='company',
            field=models.CharField(max_length=100),
        ),
    ]
