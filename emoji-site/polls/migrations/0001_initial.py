# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-20 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emoji',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('emoji', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=18)),
            ],
        ),
        migrations.AddField(
            model_name='emoji',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.User'),
        ),
    ]