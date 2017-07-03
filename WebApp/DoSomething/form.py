import random

from django.shortcuts import get_object_or_404

from .models import Category, Type


class RandomCategoryForm:

    # Random Categories
    categories = []

    # Random Distance
    ranges = []

    # Random Price
    prices = []

    def __init__(self,post):
        self.price = []
        self.ranges = []
        self.categories = []
        self.__init_categories(post)
        self.__init_distance(post)
        self.__init_price(post)

    def __init_categories(self,post):
        if self.__is_checked(post.get("food_and_restaurant")):
            self.categories.append("food_and_restaurant")

        if self.__is_checked(post.get("recreation")):
            self.categories.append("recreation")

        if self.__is_checked(post.get("events")):
            self.categories.append("events")

        if self.__is_checked(post.get("points_of_interest")):
            self.categories.append("points_of_interest")

    def __init_distance(self,post):
        if self.__is_checked(post.get("five_check_box")):
            self.ranges.append(5)

        if self.__is_checked(post.get("ten_check_box")):
            self.ranges.append(10)

        if self.__is_checked(post.get("fifteen_five_check_box")):
            self.ranges.append(15)

        if self.__is_checked(post.get("twenty_check_box")):
            self.ranges.append(20)

    def __init_price(self,post):
        if self.__is_checked(post.get("free_check_box")):
            self.prices.append(0)

        if self.__is_checked(post.get("inexpensive_check_box")):
            self.prices.append(1)

        if self.__is_checked(post.get("moderate_five_check_box")):
            self.prices.append(2)

        if self.__is_checked(post.get("expensive_check_box")):
            self.prices.append(3)

    def __is_checked(self, boolean):
        if boolean != None:
            return True
        return False

    def get_random_categories(self):

        rand1 = random.randint(0,len(self.categories)-1)
        rand2 = random.randint(0, len(self.ranges) - 1)
        rand3 = random.randint(0, len(self.prices)-1)

        return self.categories[rand1], self.ranges[rand2] * 1000, self.prices[rand3]