# Generated by Django 5.0.7 on 2025-01-28 18:50
import json
import os

from django.db import migrations, models

import json
import os

from django.db import migrations

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IdolDatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idol_name', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('birthdate', models.DateField()),
                ('birthplace', models.CharField(max_length=50)),
                ('zodiac', models.CharField(max_length=50)),
                ('height', models.CharField(max_length=50)),
                ('sns', models.CharField(max_length=200)),
            ],
        ),
    ]