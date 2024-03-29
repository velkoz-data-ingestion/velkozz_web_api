# Generated by Django 3.1.4 on 2021-05-10 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_api', '0007_auto_20210331_0424'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndeedJobPosts',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=300)),
                ('company', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('summary', models.TextField()),
                ('date_posted', models.DateField()),
            ],
        ),
    ]
