# Generated by Django 4.2 on 2023-04-13 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0006_source_source_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
