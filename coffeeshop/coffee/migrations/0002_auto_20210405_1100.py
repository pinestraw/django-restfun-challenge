# Generated by Django 3.1.7 on 2021-04-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoptionvalue',
            name='value',
            field=models.CharField(max_length=20),
        ),
    ]
