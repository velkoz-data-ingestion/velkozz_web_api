# Generated by Django 3.1.4 on 2021-12-10 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography_api', '0007_auto_20210925_0745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name_plural': 'Countries'},
        ),
    ]