# Generated by Django 3.1.4 on 2021-09-25 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geography_api', '0004_auto_20210925_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='capital',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
