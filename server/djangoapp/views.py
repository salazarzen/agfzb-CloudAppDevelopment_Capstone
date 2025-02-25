from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index_page(request):
    return render(request, 'djangoapp/index.html')

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3548b6ed-2ccc-4890-9af4-70d7ac9bad36/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)
        # return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3548b6ed-2ccc-4890-9af4-70d7ac9bad36/dealership-package/get-review"
        url_dealership = "https://us-south.functions.appdomain.cloud/api/v1/web/3548b6ed-2ccc-4890-9af4-70d7ac9bad36/dealership-package/get-dealership"
        # Get review from the URL
        reviews = get_dealer_reviews_from_cf(url, id=id)
        dealer = get_dealer_by_id(url_dealership, id=id)
        context["reviews_list"] = reviews
        context["dealer"] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)
        # return HttpResponse(all_reviews)

# Create a `add_review` view to submit a review
def add_review(request, id):
    if request.method == 'GET':
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3548b6ed-2ccc-4890-9af4-70d7ac9bad36/dealership-package/get-dealership"
        dealer = get_dealer_by_id(url, id=id)
        context["dealer"] = dealer
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            url = 'https://us-south.functions.appdomain.cloud/api/v1/web/3548b6ed-2ccc-4890-9af4-70d7ac9bad36/dealership-package/post-review'
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            review = {
                "name": request.user.username,
                "dealership": id,
                "id": id,
                "review": request.POST["content"],
                "purchase_date": request.POST["purchasedate"],
                "car_make": car.carmake.name,
                "car_model": car.name,
                "car_year": int(car.pub_date.strftime("%Y"))
            }
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    review["purchase"] = True
                else:
                    review["purchase"] = False
            payload = {}
            payload["review"] = review
            post_request(url, payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)

