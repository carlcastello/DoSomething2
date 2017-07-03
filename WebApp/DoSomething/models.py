# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length = 100,
        blank = False,
        unique = True,
    )
    def __str__(self):
        return self.name.title()

class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.name.title()

class Location(models.Model):
    address = models.CharField(
        max_length=100
    )
    latitude = models.FloatField(
        default=0
    )
    longitude = models.FloatField(
        default=0
    )
    def __str__(self):
        return self.address

class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=100,
        blank=False,
    )
    description = models.TextField(

    )
    location = models.ForeignKey(
        Location
    )
    url = models.URLField(
        max_length=200
    )
    start_datetime = models.DateTimeField(

    )
    end_datetime = models.DateTimeField(

    )

    def __str__(self):
        return self.name.title()

class Place(models.Model):
    place_id = models.CharField(
        max_length=200,
    )
    name = models.CharField(
        max_length=200
    )
    phone_number = models.CharField(
        max_length=200,
        blank=True
    )
    rating = models.FloatField(
        default=0.0
    )
    website = models.URLField(
        max_length=200,
        blank=True
    )
    category = models.ForeignKey(
        Category
    )
    location = models.ForeignKey(
        Location
    )

    def __str__(self):
        return self.place_id

    class Meta:
        unique_together = ("place_id","category")

class OpeningHour(models.Model):
    sunday = models.CharField(
        max_length=100
    )
    monday = models.CharField(
        max_length=100
    )
    tuesday = models.CharField(
        max_length=100
    )
    wednesday = models.CharField(
        max_length=100
    )
    thursday = models.CharField(
        max_length=100
    )
    friday = models.CharField(
        max_length=100
    )
    saturday = models.CharField(
        max_length=100
    )
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
    )

class Image(models.Model):
    link = models.URLField(
        max_length=100
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
    )

class Review(models.Model):
    rating = models.FloatField(

    )
    text = models.TextField(

    )
    time = models.IntegerField(

    )
    author_url = models.URLField(
        max_length=200
    )
    author_name = models.CharField(
        max_length=100
    )
    relative_time_description = models.CharField(
        max_length=100
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
    )
