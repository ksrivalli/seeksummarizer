# Generated by Django 2.2 on 2021-06-19 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Summarizer', '0003_auto_20210615_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='all_sum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=2000)),
            ],
        ),
    ]
