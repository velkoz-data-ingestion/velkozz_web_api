# Generated by Django 3.1.4 on 2021-04-20 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_api', '0007_auto_20210304_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='WallStreetBetsTickerMentions',
            fields=[
                ('day', models.DateField(primary_key=True, serialize=False, unique=True)),
                ('tickers', models.TextField()),
            ],
            options={
                'ordering': ['day'],
            },
        ),
    ]