# Generated by Django 2.1 on 2018-10-17 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(blank=True, default=18, null=True, verbose_name='年龄'),
        ),
    ]
