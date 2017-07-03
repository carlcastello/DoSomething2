# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import TemplateView, ListView

from django.http import Http404

from django.contrib.gis.geoip import GeoIP

from .form import RandomCategoryForm

from .models import Category,Type, Event, Place

# from django.contrib.gis.geos import GEOSGeometry

from GoogleAPIWrapper import GoogleSearch

from math import sin, cos, sqrt, atan2, radians

# Create your views here.
class HomeView(TemplateView):
    template_name = "DoSomething/home.html"
    geo_ip = GeoIP()

    def post(self,request,**kwargs):
        random_form = RandomCategoryForm(request.POST)
        category, distance, price = random_form.get_random_categories()


        client_ip = self.__get_client_ip(self.request)
        latitude = None
        longitude = None
        try:
            latitude, longitude = self.geo_ip.lat_lon(client_ip)
        except TypeError:
            # Mock Location
            latitude, longitude = (53.459971, -113.377110)
        # print category, distance, price

        id = None
        category_type = None
        if category == "events":
            # Search Through Events
            event = Event.objects.all().order_by('?').first()
            if event:
                event_latitude = event.location.latitude
                event_longitude = event.location.longitude
                return redirect("DoSomething:event_view",event_latitude,event_longitude)
            return redirect("DoSomething:event_view")
            pass
        else:
            category = get_object_or_404(Category, name=category)

            search = GoogleSearch(latitude=53.459971, longitude=-113.377110, radius=distance, category=category)
            place = search.execute_search()

            place_id = place.place_id
            return redirect("DoSomething:detail_view",place_id,category.name)

    def __get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class DetailView(TemplateView):
    template_name = "DoSomething/detail.html"
    geo_ip = GeoIP()

    def get_context_data(self,**kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        client_ip = self.__get_client_ip(self.request)

        user_latitude = None
        user_longitude = None
        try:
            user_latitude, user_longitude = self.geo_ip.lat_lon(client_ip)
        except TypeError:
            # Mock Location
            user_latitude, user_longitude = (53.459971, -113.377110)

        category = kwargs["category"]
        id = kwargs["id"]

        category = Category.objects.get(name=category)
        place = category.place_set.get(place_id=id)
        context["place"] = place

        context["distance"] = self.__get_distance_away(
            user_latitude,
            user_longitude,
            place.location.latitude,
            place.location.longitude
        )

        return context

    def __get_distance_away(self,user_latitude,user_longitude,place_latitude,place_longitude):

        R = 6373.0

        lat1 = radians(user_latitude)
        lon1 = radians(user_longitude)
        lat2 = radians(place_latitude)
        lon2 = radians(place_longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return round(R * c, 1)

    def __get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class EventView(TemplateView):
    template_name = "DoSomething/events.html"
    geo_ip = GeoIP()

    def get_context_data(self,**kwargs):
        context = super(EventView, self).get_context_data(**kwargs)

        client_ip = self.__get_client_ip(self.request)

        longitude = None
        latitude = None

        try:
            latitude = kwargs["latitude"]
            longitude = kwargs["longitude"]
        except KeyError:
            try:
                latitude, longitude = self.geo_ip.lat_lon(client_ip)
            except TypeError:
                # Mock Location
                latitude, longitude = (53.459971, -113.377110)


        context["latitude"] = latitude
        context["longitude"] = longitude

        context["events"] = Event.objects.all()

        return context

    # https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    def __get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class CategoriesView(TemplateView):
    template_name = "DoSomething/categories.html"


class CategoryListView(ListView):
    template_name = "DoSomething/category_list.html"
    paginate_by = 30
    context_object_name = "places"
    geo_ip = GeoIP()

    def get_queryset(self):

        category = Category.objects.get(name=self.kwargs["type"])
        queryset = Place.objects.filter(category=category).order_by("-name")

        client_ip = self.__get_client_ip(self.request)

        user_latitude = None
        user_longitude = None
        try:
            user_latitude, user_longitude = self.geo_ip.lat_lon(client_ip)
        except TypeError:
            # Mock Location
            user_latitude, user_longitude = (53.459971, -113.377110)

        places = []
        for place in queryset:
            dictionary = {}
            place_latitude = place.location.latitude
            place_longitude = place.location.longitude
            dictionary[place] = self.__get_distance_away(user_latitude, user_longitude, place_latitude, place_longitude)
            places.append(dictionary)

        return places


    def get_context_data(self,**kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context["type"] = self.kwargs["type"]

        context["title"] = " ".join(self.kwargs["type"].split("_")).title()

        # context["places"] = distance
        return context

    def __get_distance_away(self,user_latitude,user_longitude,place_latitude,place_longitude):

        R = 6373.0

        lat1 = radians(user_latitude)
        lon1 = radians(user_longitude)
        lat2 = radians(place_latitude)
        lon2 = radians(place_longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return round(R * c, 1)

    def __get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

#
class DeleteView(TemplateView):
    template_name = None

    def get(self,request,**kwargs):
        Place.objects.all().delete()
        return redirect("DoSomething:home")

# class UpdateView(TemplateView):
#     template_name = None
#
#     def get(self,request,**kwargs):
#         categories = {}
#         categories["recreation"] = ["amusement_park", "aquarium", "art_gallery", "bowling_alley", "book_store", "campground", "casino", "library", "lodging", "museum", "spa"]
#         categories["night_life"] = ["bar", "night_club"]
#         categories["food_and_restaurant"] = ["bakery", "cafe", "liquor_store", "meal_delivery", "meal_takeaway", "restaurant"]
#         categories["points_of_interest"] = ["point_of_interest", "cemetery", "church", "city_hall", "local_government_office", "park", "university"]
#
#         for category in categories:
#             search = GoogleSearch(latitude=53.459971,longitude=-113.377110,radius=20000,type=None,types = categories[category])
#             search.execute_search()
#         return redirect("DoSomething:home")
#
#
class InitializeView(TemplateView):
    template_name = None

    def get(self,request,**kwargs):
        categories = {}
        categories["recreation"] = ["amusement_park","aquarium","art_gallery","bowling_alley","book_store","campground","casino","library","lodging","museum","spa"]
        categories["night_life"] = ["bar","night_club"]
        categories["food_and_restaurant"] = ["bakery", "cafe","liquor_store","meal_delivery","meal_takeaway","restaurant"]
        categories["points_of_interest"] = ["point_of_interest","cemetery","church","city_hall","local_government_office","park","university"]
        categories["todos"] = ["home_goods_store"]
        categories["random"] = []

        for key in categories:
            category = Category(name=key)
            category.save()

            for key2 in categories[key]:
                type = Type(name=key2,category=category)
                type.save()
        return redirect("DoSomething:home")
