# Generated by Django 4.2 on 2023-04-09 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0004_news_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.CharField(max_length=255),
        ),
    ]