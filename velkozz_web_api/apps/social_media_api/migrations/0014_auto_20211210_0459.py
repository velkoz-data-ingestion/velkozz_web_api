# Generated by Django 3.1.4 on 2021-12-10 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_api', '0013_redditdevapps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redditdevapps',
            name='client_id',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='redditdevapps',
            name='client_secret',
            field=models.CharField(max_length=50),
        ),
    ]
