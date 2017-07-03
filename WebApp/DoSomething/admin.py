# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Type, Event, Location, Place, OpeningHour, Image, Review

# Register your models here.
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Event)
admin.site.register(Location)

admin.site.register(Place)
admin.site.register(OpeningHour)
admin.site.register(Image)
admin.site.register(Review)

