import  random
from googleplaces import GooglePlaces, types, lang
from math import sin, cos, sqrt, atan2, radians
from .models import Place, Review, OpeningHour, Review, Type, Location, Category
from django.core.exceptions import ObjectDoesNotExist

# class Search(object):
#     GOOGLE_PLACE = None
#     API_KEY = 'AIzaSyADrWqVV6DvGHiBRLPuy6UosGFIHwApLqo'
#
#     latitude = None
#     longitude = None
#
#     query_result = None
#
#     place = None
#
#     def __init__(self,latitude,longitude):
#         self.GOOGLE_PLACE = GooglePlaces(self.API_KEY)
#         self.latitude = latitude
#         self.longitude = longitude
#
#
#     def execute(self,keyword,type,radius,price):
#         self.query_result = self.GOOGLE_PLACE.nearby_search(
#             lat_lng={"lat":self.latitude,"lng":self.longitude},
#             keyword=keyword,
#             type=type,
#             radius=radius[1] * 1000,
#         )
#         # print self.queryreturn_result.places
#
#     def to_string(self):
#         dictionary = {}
#         details = self.place.details
#
#         dictionary["place_id"] = details["place_id"]
#
#
#         dictionary["name"] = details["name"]
#
#         # print details["formatted_phone_number"]
#         try:
#             dictionary["rating"] = range(0,int(round(details["rating"])))
#
#             dictionary["phone_number"] = details["formatted_phone_number"]
#
#             dictionary["website"] = details["website"]
#
#             dictionary["reviews"] = details["reviews"]
#
#             hours = {}
#             weekday = []
#             for day in details["opening_hours"]["weekday_text"]:
#                 weekday.append(day.split(":",1))
#             hours["weekday_text"] = weekday
#             dictionary["opening_hours"] = hours
#         except KeyError:
#             pass
#
#
#         dictionary["location"] = {}
#         dictionary["location"]["address"] = details["formatted_address"]
#         dictionary["location"]["lat"] = float(details["geometry"]["location"]["lat"])
#         dictionary["location"]["lng"] = float(details["geometry"]["location"]["lng"])
#
#         dictionary["distance"] = self.__get_distance_away()
#
#
#
#         return dictionary
#
#     def get_photos(self):
#         photos = []
#         for photo in self.place.photos:
#             # print photo
#             photo.get(maxheight=300, maxwidth=550)
#             photos.append(photo.url)
#         return photos
#
#     # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
#     def __get_distance_away(self):
#
#         R = 6373.0
#         details = self.place.details
#
#         lat1 = radians(self.latitude)
#         lon1 = radians(self.longitude)
#         lat2 = radians(details["geometry"]["location"]["lat"])
#         lon2 = radians(details["geometry"]["location"]["lng"])
#
#         dlon = lon2 - lon1
#         dlat = lat2 - lat1
#
#         a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#         return str(round(R * c, 1)) + " km"


class GoogleSearch:
    GOOGLE_PLACE = None
    API_KEY = 'AIzaSyADrWqVV6DvGHiBRLPuy6UosGFIHwApLqo'

    radius = None
    latitude = None
    longitude = None
    types = None

    category = None

    query_result = None

    def __init__(self, latitude, longitude, radius, types=None, category=None):
        self.GOOGLE_PLACE = GooglePlaces(self.API_KEY)
        self.radius = radius
        self.latitude = latitude
        self.longitude = longitude
        self.types = types
        self.category = category

    def execute_search(self):
        sets = {}
        # print self.type, self.type is not None

        if self.category is not None:
            # Search by Type
            places = []
            # Top 3 types
            while len(places) == 0:
                type = Type.objects.all().filter(category=self.category).order_by('?').first()
                query = self.GOOGLE_PLACE.nearby_search(
                        lat_lng={"lat":self.latitude,"lng":self.longitude},
                        type=type.name,
                        radius=self.radius,
                    )
                places = query.places
            sets[type.name] = places

            return self.__get_place(sets)


    def __get_place(self, sets):
        for type in sets:
            places = sets[type]

            rand = random.randint(0,len(places)-1)
            place = places[rand]

            category = Type.objects.get(name=type).category
            try:
                category.place_set.get(place_id=place.place_id)
            except ObjectDoesNotExist:
                self.__save_place(place, type)

            return place
        # print category
        # category = Category.objects.get(name=type)
        # place = category.place_set.get(place_id=id)
        # if Place.objects.get(id)

    # def __get_places(self, sets):
    #     # Convert Google Place to Django Place Model
    #     for type in sets:
    #         # print sets[type].places
    #         for place in sets[type]:
    #             self.__save_place(place, type)

    def __save_place(self, place, type):

        # print place
        place.get_details()
        # print place.details
        # place = place.get_details()
        place_detail = place.details
        # print place_detail

        address = place_detail["formatted_address"]
        latitude = place_detail["geometry"]["location"]["lat"]
        longitude = place_detail["geometry"]["location"]["lng"]
        location = Location(
            address=address,
            latitude=latitude,
            longitude=longitude
        )
        location.save()
        # print place_detail
        id = place_detail["place_id"].encode('utf-8')
        name = place_detail["name"].encode('utf-8')
        phone_number = ""
        rating = 0.0
        website = ""
        category = Type.objects.get(name=type).category

        try:
            phone_number = place_detail["formatted_phone_number"].encode('utf-8')
        except:
            pass

        try:
            rating = place_detail["rating"].encode('utf-8')
        except:
            pass

        try:
            website = place_detail["website"].encode('utf-8')
        except:
            pass

        place = Place(
            place_id=id,
            name=name,
            phone_number=phone_number,
            rating=rating,
            website=website,
            category=category,
            location=location
        )
        place.save()

        #  This Handles Review
        try:
            for place_review in place_detail["reviews"]:
                review = Review(
                    rating=place_review["rating"].encode('utf-8'),
                    text=place_review["text"].encode('utf-8'),
                    time=place_review["time"].encode('utf-8'),
                    author_url=place_review["author_url"].encode('utf-8'),
                    author_name=place_review["author_name"].encode('utf-8'),
                    relative_time_description=place_review["relative_time_description"].encode('utf-8'),
                    place=place
                )
                review.save()
        except:
            pass

        # Handles Opening Hours
        try:
            monday = None
            tuesday = None
            wednesday = None
            thursday = None
            friday = None
            saturday = None
            sunday = None

            for day in place_detail["opening_hours"]["weekday_text"]:
                schedule = day.split(":", 1)
                if schedule[0] == "Monday":
                    monday = schedule[1].encode('utf-8')
                elif schedule[0] == "Tuesday":
                    tuesday = schedule[1].encode('utf-8')
                elif schedule[0] == "Wednesday":
                    wednesday = schedule[1].encode('utf-8')
                elif schedule[0] == "Thursday":
                    thursday = schedule[1].encode('utf-8')
                elif schedule[0] == "Friday":
                    friday = schedule[1].encode('utf-8')
                elif schedule[0] == "Saturday":
                    saturday = schedule[1].encode('utf-8')
                elif schedule[0] == "Sunday":
                    sunday = schedule[1].encode('utf-8')

            opening_hours = OpeningHour(
                monday=monday,
                tuesday=tuesday,
                wednesday=wednesday,
                thursday=thursday,
                friday=friday,
                saturday=saturday,
                sunday=sunday,
                place=place
            )
            opening_hours.save()

        except:
            print "Error Saving Hours"
            pass


            # Handles Images
