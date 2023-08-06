import json
import os
from datetime import datetime
from random import choice

import rstr
import yaml
from faker import Faker
from faker.providers import BaseProvider
from faker_vehicle import VehicleProvider as VP
from russian_names import RussianNames


class FlowerProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/data/plants.yml") as f:
            d = yaml.load(f, Loader=yaml.SafeLoader)
            self.flower_names = d["flowers"]["names"]
            self.flavors = d["flowers"]["flavors"]
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def flower(self, locale=None):
        return {
            "Name": choice(self.flower_names),
            "Color": self.fake.color_name(),
            "Flavor": choice(self.flavors),
            "Location": self.fake.location_on_land()[2:]
        }


class VehicleProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()
        self.fake.add_provider(VP)

    def vehicle(self, locale=None):
        if locale in [None, "en_US"]:
            locale = "en_US"
            name = self.fake.name()
            plate = self.fake.license_plate()
        elif locale == 'ru_TL':
            name = RussianNames(count=1, gender=0.5,
                                transliterate=True).get_batch()[0]
            plate = rstr.xeger(r'[АВЕКМНОРСТУХ]{2}\d{3}[АВЕКМНОРСТУХ]')

        return {
            **self.fake.vehicle_object(),
            **{
                "Plate": plate,
                "Owner": name
            }
        }


class BookProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        self.word_list = [
            "interesting", "story", "of", "the",
            "dummy", "doll", "steve", "known", "as", "boredom",
            "slayer", "that", "whished", "to", "make", "everybody", "happy",
            "without", "being", "imprisoned", "in", "alcatraz", "at", "the", "end"
        ]
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def book(self, locale=None, word_list=None):
        if locale in [None, "en_US"]:
            locale = "en_US"
            author = self.fake.name()
        elif locale == 'ru_TL':
            author = RussianNames(count=1, gender=0.5,
                                  transliterate=True).get_batch()[0]
        word_list = word_list if word_list is not None else self.word_list

        return {
            "Author": author,
            "Name": self.fake.sentence(nb_words=3, ext_word_list=word_list),
            "Year": self.fake.random_int(1700, 2020),
            "Pages": self.fake.random_int(50, 5000)
        }


class BookkeepingProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def record(self, locale=None):
        if locale in [None, "en_US"]:
            locale = "en_US"
            name = self.fake.name()
            salary = self.fake.random_number(digits=4, fix_len=True)
        elif locale == 'ru_TL':
            name = RussianNames(count=1, gender=0.5,
                                transliterate=True).get_batch()[0]
            salary = self.fake.random_number(digits=5, fix_len=True)

        return {
            "Name": name,
            "Job": self.fake.job(),
            "Project": self.fake.catch_phrase(),
            "Salary": salary
        }


class TeacherProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/data/education.yml") as f:
            d = yaml.load(f, Loader=yaml.SafeLoader)
            self.ranks = d["university"]["ranks"]
            self.degrees = d["university"]["degrees"]
            self.faculties = d["university"]["faculties"]
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def teacher(self, locale='en_US'):
        if locale in [None, "en_US"]:
            locale = "en_US"
            name = self.fake.name()
        elif locale == 'ru_TL':
            name = RussianNames(count=1, gender=0.5,
                                transliterate=True).get_batch()[0]

        return {
            "Name": name,
            "Faculty": choice(self.faculties),
            "Rank": choice(self.ranks[locale]),
            "Degree": choice(self.degrees[locale])
        }


class StudentProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/data/education.yml") as f:
            d = yaml.load(f, Loader=yaml.SafeLoader)
            self.faculties = d["university"]["faculties"]
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def student(self, locale='en_US'):
        if locale in [None, "en_US"]:
            locale = "en_US"
            name = self.fake.name()
        elif locale == 'ru_TL':
            name = RussianNames(count=1, gender=0.5,
                                transliterate=True).get_batch()[0]

        return {
            "Name": name,
            "Faculty": choice(self.faculties),
            "Group": self.fake.random_number(digits=3, fix_len=True),
            "AvgScore": self.fake.random_int(1, 10)
        }


class SportsmanProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/data/sport.yml") as f:
            d = yaml.load(f, Loader=yaml.SafeLoader)
            self.sports = d["olympic"]["sports"]
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def sportsman(self, locale=None):
        gender_dict = {
            "name_female": 0.,
            "name_male": 1.
        }
        gender = choice(["name_female", "name_male"])
        season = choice(["summer", "winter"])
        if locale in [None, "en_US"]:
            locale = "en_US"
            name = getattr(self.fake, gender)()
        elif locale == 'ru_TL':
            name = RussianNames(count=1, gender=gender_dict[gender],
                                transliterate=True).get_batch()[0]
        if gender == "name_female":
            height = self.fake.random_int(145, 200)
            weight = self.fake.random_int(45, 85)
        else:
            height = self.fake.random_int(160, 215)
            weight = self.fake.random_int(60, 120)

        return {
            "Name": name,
            "Age": self.fake.random_int(18, 40),
            "Height": height,
            "Weight": weight,
            "Sport": choice(self.sports[season]),
            "Season": season
        }


class SoldierProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/data/army.yml") as f:
            d = yaml.load(f, Loader=yaml.SafeLoader)
            self.ranks = d["ranks"]
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def soldier(self, locale='en_US'):
        if locale in [None, "en_US"]:
            locale = "en_US"
            name = self.fake.name()
        elif locale == 'ru_TL':
            name = RussianNames(count=1, gender=0.9,
                                transliterate=True).get_batch()[0]
        rank_type = choice(["non_officer", "officer"])

        return {
            "Name": name,
            "Rank": choice(self.ranks[locale][rank_type]),
            "Company": self.fake.random_number(digits=5, fix_len=True),
            "Age": self.fake.random_int(18, 55)
        }


class ShipmentProvider(BaseProvider):
    def __init__(self, generator):
        super().__init__(generator)
        self.word_list = [
            "toilet", "paper", "sharp", "razor", "chocolate", "meat",
            "spray", "cleaning", "matches", "green", "apple", "computers",
            "cables", "connectors"
        ]
        Faker.seed(int(round(datetime.now().timestamp() * 1000)))
        self.fake = Faker()

    def shipment(self, word_list=None, locale=None):
        count = self.fake.random_int(100, 10000)
        price = count * self.fake.random_int(10, 10000)
        word_list = word_list if word_list is not None else self.word_list

        return {
            "Name": self.fake.sentence(nb_words=2, ext_word_list=word_list),
            "Country": self.fake.country(),
            "Count": count,
            "Price": price
        }
