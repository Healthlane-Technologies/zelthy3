# Generated by Django 4.2.2 on 2023-07-29 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_models', '0005_framemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='framemodel',
            name='timestamp',
            field=models.DateField(null=True),
        ),
    ]
