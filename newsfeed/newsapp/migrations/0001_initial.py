# Generated by Django 4.1.6 on 2023-04-01 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_title', models.CharField(max_length=30)),
                ('last_name', models.URLField()),
            ],
        ),
    ]
