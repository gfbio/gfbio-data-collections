# Generated by Django 3.2.13 on 2022-07-29 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='validation_schema',
            field=models.JSONField(default=list),
        ),
    ]