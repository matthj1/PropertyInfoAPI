# https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E475&maxBedrooms=3&minBedrooms=1&maxPrice=270000&sortType=6&propertyTypes=bungalow%2Cdetached%2Cflat%2Cland%2Cpark-home%2Csemi-detached%2Cterraced&includeSSTC=false&mustHave=garden%2Cparking&dontShow=newHome%2Cretirement%2CsharedOwnership&furnishTypes=&keywords=

import requests
from bs4 import BeautifulSoup
import re
import datetime
import csv
import json


class RightMoveScrapper:

    URL_initial = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier="

    def __init__(self, **kwargs):
        self.search_area = kwargs.get("search_area")
        self.max_bedrooms = kwargs.get("max_bedrooms", None)
        self.min_bedrooms = kwargs.get("min_bedrooms", None)
        self.max_price = kwargs.get("max_price", None)
        self.min_price = kwargs.get("min_price", None)
        self.show_house_type = kwargs.get("show_house_type")
        self.must_have = kwargs.get("must_have")
        self.dont_show = kwargs.get("dont_show")

    def build_url(self, page_number):
        def populate_house_type(house_types):
            output_sting = "&propertyTypes="
            if house_types:
                output_sting = output_sting + "%2C".join(house_types)
                return output_sting
            else:
                return ""

        def populate_must_have(must_haves):
            output_sting = "&mustHave="
            if must_haves:
                output_sting = output_sting + "%2C".join(must_haves)
                return output_sting
            else:
                return ""

        def populate_dont_show(dont_show):
            output_sting = "&dontShow="
            if dont_show:
                output_sting = output_sting + "%2C".join(dont_show)
                return output_sting
            else:
                return ""

        if self.search_area:
            self.URL_initial = self.URL_initial + self.search_area
        if self.max_bedrooms:
            self.URL_initial = self.URL_initial + "&maxBedrooms={}".format(self.max_bedrooms)
        if self.min_bedrooms:
            self.URL_initial = self.URL_initial + "&minBedrooms={}".format(self.min_bedrooms)
        if self.max_price:
            self.URL_initial = self.URL_initial + "&maxPrice={}".format(self.max_price)
        if self.min_price:
            self.URL_initial = self.URL_initial + "&minPrice={}".format(self.min_price)
        self.URL_initial = self.URL_initial + "&index={}".format(page_number)
        self.URL_initial = self.URL_initial + populate_house_type(self.show_house_type)
        self.URL_initial = self.URL_initial + populate_must_have(self.must_have)
        self.URL_initial = self.URL_initial + populate_dont_show(self.must_have)
        print(self.URL_initial)
        return self.URL_initial

    def scrape(self):

        URL_to_scrape = self.build_url(0)
        completed_all_pages = False
        page_index = 0
        output_dict = {}

        def get_date(date_string):
            if "Added" in date_string:
                if "today" in date_string:
                    date = datetime.date.today()
                    return date
                elif "yesterday" in date_string:
                    date = datetime.date.today() - datetime.timedelta(days=1)
                    return date
                else:
                    year = int(date_string[15:])
                    if date_string[12] == "0":
                        month = int(date_string[13])
                    else:
                        month = int(date_string[12:14])
                    if date_string[9] == "0":
                        day = int(date_string[10])
                    else:
                        day = int(date_string[9:11])
                    date = datetime.date(year, month, day)
                    return date
            elif "Reduced" in date_string:
                if "today" in date_string:
                    date = datetime.date.today()
                    return date
                elif "yesterday" in date_string:
                    date = datetime.date.today() - datetime.timedelta(days=1)
                    return date
                else:
                    year = int(date_string[17:])
                    if date_string[14] == "0":
                        month = int(date_string[15])
                    else:
                        month = int(date_string[14:16])
                    if date_string[11] == "0":
                        day = int(date_string[12])
                    else:
                        day = int(date_string[11:13])
                    date = datetime.date(year, month, day)
                    return date

        def get_house_type(house_string):
            semi_find = re.compile("semi-detached")
            detached_find = re.compile("\sdetached")
            if "flat" in house_string:
                return "flat"
            elif semi_find.search(house_string):
                return "semi-detached"
            elif detached_find.search(house_string):
                return "detached"
            elif "terraced" in house_string:
                return "terraced"
            else:
                return "Unknown"

        while not completed_all_pages:
            opening_page = requests.get(URL_to_scrape)
            opening_page_content = opening_page.content
            opening_page_soup = BeautifulSoup(opening_page_content, features="lxml")

            property_cards = opening_page_soup.find_all("div", {"id": re.compile("property-[0-9]+")})

            for index, house in enumerate(property_cards):
                try:
                    if "Featured Property" in house.find("div", {"class": "propertyCard-moreInfoFeaturedTitle"}):
                        featured = True
                    else:
                        featured = False
                    ref_number = house.find("a", {"class", "propertyCard-additionalImgs"}).get("href")[28:36]
                    price = house.find("div", {"class": "propertyCard-priceValue"}).contents[0].strip()
                    num_rooms = house.find("h2", {"class": "propertyCard-title"}).contents[0].strip()[0]
                    listed_date_search = house.find("span", {"class", "propertyCard-contactsAddedOrReduced"})
                    date = get_date(listed_date_search.contents[0])
                    postcode = house.find("address", {"class": "propertyCard-address"}).span.contents[0].split(",")[-1].strip()
                    house_type_search = house.find("h2", {"class": "propertyCard-title"})
                    house_type = get_house_type(house_type_search.contents[0].strip())
                    if not featured:
                        house_details = {"Reference": ref_number,
                                         "Price": price,
                                         "Number of Rooms": num_rooms,
                                         "House Type": house_type,
                                         "Date Listed": date,
                                         "Postcode": postcode
                                         }
                        output_dict[ref_number] = house_details
                        for a, b in house_details.items():
                            print(a, b)
                except TypeError:
                    completed_all_pages = True
                    print("Finished!")
                    return output_dict
            page_index = page_index + 24
            URL_to_scrape = self.build_url(page_index)
            print("I'm on page " + str(page_index/24))



example_search = {
    "search_area": "REGION%5E475",
    "max_bedrooms": 3,
    "min_bedrooms": 1,
    "max_price": 280000,
    "min_price": None,
    "show_house_type": ["flat", "detached", "semi-detached", "terraced"],
    "must_have": [],
    "dont_show": []
}

x = RightMoveScrapper(**example_search)

x.scrape()
