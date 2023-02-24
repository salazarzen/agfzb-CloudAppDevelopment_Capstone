from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='car name')
    description = models.CharField(max_length=1000)
    doors = models.IntegerField(default=4)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=4)
    name = models.CharField(null=False, max_length=30, default='model name')

    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPE = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON')
    ]
    car_type = models.CharField(max_length=7, choices=CAR_TYPE, default=SEDAN)
    pub_date = models.DateField(null=True)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Type: " + self.car_type

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date="", car_make="", car_model="", car_year="", sentiment="", id=""):
        # dealership
        self.dealership = dealership
        # Review name
        self.name = name
        # Dealer purchase
        self.purchase = purchase
        # Dealer review
        self.review = review

    def __str__(self):
        return "Review: " + self.full_name
