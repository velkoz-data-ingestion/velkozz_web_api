# Generated by Django 3.1.4 on 2021-06-04 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_api', '0002_auto_20210604_0328'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsarticles',
            old_name='url',
            new_name='article_url',
        ),
    ]