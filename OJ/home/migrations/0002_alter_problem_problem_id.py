# Generated by Django 5.1.6 on 2025-05-24 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='problem_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
