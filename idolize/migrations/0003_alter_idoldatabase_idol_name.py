# Generated by Django 5.0.7 on 2025-01-30 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idolize', '0002_alter_idoldatabase_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idoldatabase',
            name='idol_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
