# Generated by Django 3.1.4 on 2021-08-12 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_api', '0010_dailyyoutubechannelstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyyoutubechannelstats',
            name='channel_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
