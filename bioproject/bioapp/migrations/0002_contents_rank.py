# Generated by Django 2.1.7 on 2020-07-01 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bioapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contents',
            name='rank',
            field=models.IntegerField(default=-1),
        ),
    ]
