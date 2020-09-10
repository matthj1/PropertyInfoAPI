# https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E475&maxBedrooms=3&minBedrooms=1&maxPrice=270000&sortType=6&propertyTypes=bungalow%2Cdetached%2Cflat%2Cland%2Cpark-home%2Csemi-detached%2Cterraced&includeSSTC=false&mustHave=garden%2Cparking&dontShow=newHome%2Cretirement%2CsharedOwnership&furnishTypes=&keywords=

import requests
from bs4 import BeautifulSoup
import re
import datetime
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

        URL_to_build = self.URL_initial

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

        def round_price(price, min_max):
            list_of_prices = [50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000,
                              170000,
                              175000, 180000, 190000, 200000, 210000, 220000, 230000, 240000, 250000, 260000, 270000,
                              280000,
                              290000, 300000, 325000, 350000, 375000, 400000, 425000, 450000, 475000, 500000, 550000,
                              600000,
                              650000, 700000, 800000, 900000, 1000000, 1250000, 1500000, 1750000, 2000000, 2500000,
                              3000000,
                              4000000, 5000000, 7500000, 10000000, 15000000, 20000000]
            for position, price_item in enumerate(list_of_prices):
                if min_max == "max":
                    if price < price_item:
                        return list_of_prices[position + 1]
                else:
                    if price < price_item:
                        return list_of_prices[position]

        if self.search_area:
            URL_to_build = URL_to_build + self.search_area
        if self.max_bedrooms:
            URL_to_build = URL_to_build + "&maxBedrooms={}".format(self.max_bedrooms)
        if self.min_bedrooms:
            URL_to_build = URL_to_build + "&minBedrooms={}".format(self.min_bedrooms)
        if self.max_price:
            URL_to_build = URL_to_build + "&maxPrice={}".format(round_price(self.max_price, "max"))
        if self.min_price:
            URL_to_build = URL_to_build + "&minPrice={}".format(round_price(self.min_price, "min"))
        URL_to_build = URL_to_build + "&index={}".format(page_number)
        URL_to_build = URL_to_build + populate_house_type(self.show_house_type)
        URL_to_build = URL_to_build + populate_must_have(self.must_have)
        URL_to_build = URL_to_build + populate_dont_show(self.must_have)
        print(URL_to_build)
        return URL_to_build

    def scrape(self):

        page_index = 0
        URL_to_scrape = self.build_url(page_index)
        completed_all_pages = False
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
            if "flat" in house_string.lower():
                return "flat"
            elif semi_find.search(house_string.lower()):
                return "semi-detached"
            elif detached_find.search(house_string.lower()):
                return "detached"
            elif "terraced" in house_string.lower():
                return "terraced"
            elif "bungalow" in house_string.lower():
                return "bungalow"
            elif "land" in house_string.lower():
                return "land"
            elif "park-home" in house_string.lower():
                return "park-home"
            else:
                return "Unknown"

        def parse_postcode(postcode):
            postcode_parser = re.compile("[A-Z]{2}\d{1,2}(\s\d[A-Z][A-Z])?")
            try:
                return re.search(postcode_parser, postcode).group(0)
            except AttributeError:
                return None

        def get_coordinates(reference):
            try:
                URL_BASE = "https://www.rightmove.co.uk/property-for-sale/property-"
                urlCoordinates = URL_BASE + str(reference) + ".html"
                print(urlCoordinates)
                pageHTML = requests.get(urlCoordinates).content
                pageSoup = BeautifulSoup(pageHTML, features="lxml")
                coordinateIn = str(pageSoup.find("a", {"class": "block js-tab-trigger js-ga-minimap"}))
                findLatitude = re.compile("latitude=-?\d+\.\d+")
                latitude = findLatitude.findall(coordinateIn)[0].split("=")[1]
                findLongitude = re.compile("longitude=-?\d+\.\d+")
                longitude = findLongitude.findall(coordinateIn)[0].split("=")[1]
                return [float(latitude), float(longitude)]
            except:
                print("Error with coordinates")
                return None

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
                    try:
                        price = int(house.find("div", {"class": "propertyCard-priceValue"}).contents[0].strip()[1:].replace(",", ""))
                    except ValueError:
                        price = None
                    num_rooms = int(house.find("h2", {"class": "propertyCard-title"}).contents[0].strip()[0])
                    date = get_date(house.find("span", {"class", "propertyCard-contactsAddedOrReduced"}).contents[0])
                    postcode = parse_postcode(house.find("address", {"class": "propertyCard-address"}).span.contents[0])
                    if postcode:
                        location_if_not_postcode = None
                    else:
                        location_if_not_postcode = house.find("address", {"class": "propertyCard-address"}).span.contents[0].split(",")[-1].strip()
                    house_type_search = house.find("h2", {"class": "propertyCard-title"})
                    house_type = get_house_type(house_type_search.contents[0].strip())
                    if not featured:
                        house_details = {"Reference": ref_number,
                                         "Price": price,
                                         "Number of Rooms": num_rooms,
                                         "House Type": house_type,
                                         "Date Listed": date.strftime("%d/%m/%Y"),
                                         "Postcode": postcode,
                                         "LocationNoPc": location_if_not_postcode,
                                         "Coordinates": get_coordinates(ref_number)
                                         }
                        output_dict[ref_number] = house_details
                        for a, b in house_details.items():
                            print(a + ": ", b)
                        print("\n")
                except TypeError:
                    completed_all_pages = True
                    with open("Edinburgh_Data.json", "w") as json_file:
                        print("got here")
                        json.dump(output_dict, json_file)
                    print("Finished!")
                    return output_dict
                except IndexError:
                    print("Something wrong with the scrape. Please try again")
                    return "Something wrong with the scrape. Please try again"
            page_index = page_index + 24
            URL_to_scrape = self.build_url(page_index)
            print("I'm on page " + str(page_index/24))


if __name__ == "__main__":

    example_search = {
        "search_area": "REGION%5E475",
        "max_bedrooms": 2,
        "min_bedrooms": 2,
        "max_price": 250000,
        "min_price": 230000,
        "show_house_type": ["flat", "detached", "semi-detached", "terraced"],
        "must_have": [],
        "dont_show": ["newHome"]
    }

    x = RightMoveScrapper(**example_search)

    x.scrape()
