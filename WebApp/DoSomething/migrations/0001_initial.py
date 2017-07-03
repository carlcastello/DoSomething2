# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-03 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OpeningHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sunday', models.CharField(max_length=100)),
                ('monday', models.CharField(max_length=100)),
                ('tuesday', models.CharField(max_length=100)),
                ('wednesday', models.CharField(max_length=100)),
                ('thursday', models.CharField(max_length=100)),
                ('friday', models.CharField(max_length=100)),
                ('saturday', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=200)),
                ('rating', models.FloatField(default=0.0)),
                ('website', models.URLField(blank=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DoSomething.Category')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DoSomething.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('text', models.TextField()),
                ('time', models.IntegerField()),
                ('author_url', models.URLField()),
                ('author_name', models.CharField(max_length=100)),
                ('relative_time_description', models.CharField(max_length=100)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DoSomething.Place')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DoSomething.Category')),
            ],
        ),
        migrations.AddField(
            model_name='openinghour',
            name='place',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='DoSomething.Place'),
        ),
        migrations.AddField(
            model_name='image',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DoSomething.Place'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DoSomething.Location'),
        ),
        migrations.AlterUniqueTogether(
            name='place',
            unique_together=set([('place_id', 'category')]),
        ),
    ]