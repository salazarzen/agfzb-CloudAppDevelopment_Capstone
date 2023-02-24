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

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
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


# <HINT> Create a plain Python class `DealerReview` to hold review data
