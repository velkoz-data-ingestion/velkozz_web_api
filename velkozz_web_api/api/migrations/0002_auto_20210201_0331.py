# Generated by Django 3.1.5 on 2021-02-01 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scienceposts',
            options={'ordering': ['created_on'], 'verbose_name_plural': 'Science Subreddit Posts'},
        ),
        migrations.AlterModelOptions(
            name='wallstreetbetsposts',
            options={'ordering': ['created_on'], 'verbose_name_plural': 'WallStreetBets Subreddit Posts'},
        ),
        migrations.AlterField(
            model_name='scienceposts',
            name='author_has_verified_email',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='scienceposts',
            name='author_is_gold',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='scienceposts',
            name='author_mod',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='scienceposts',
            name='over_18',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='scienceposts',
            name='spoiler',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='scienceposts',
            name='stickied',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='wallstreetbetsposts',
            name='author_has_verified_email',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='wallstreetbetsposts',
            name='author_is_gold',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='wallstreetbetsposts',
            name='author_mod',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='wallstreetbetsposts',
            name='over_18',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='wallstreetbetsposts',
            name='spoiler',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='wallstreetbetsposts',
            name='stickied',
            field=models.BooleanField(null=True),
        ),
    ]
