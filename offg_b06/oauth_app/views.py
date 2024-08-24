from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required
import requests

import oauth_app
from .forms import SubmitHousing
from .models import Housing

# Create your views here.
from .forms import CreateUserForm
from django.utils.datastructures import MultiValueDictKeyError


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('oauth_app:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account Created for ' + user)
                return redirect('oauth_app:login')
        context = {'form': form}
        return render(request, 'oauth_app/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('oauth_app:home')
    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('oauth_app:home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'oauth_app/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('oauth_app:login')


@login_required(login_url='oauth_app:login')
def home(request):
    housing = Housing.objects.all().filter(official=True)

    if request.method == 'GET':
        if 'title' in request.GET and request.GET['title'] != '':
            housing = housing.filter(title__icontains=request.GET['title'])
        if 'beds' in request.GET and request.GET['beds'] != '':
            housing = housing.filter(bed=request.GET['beds'])
        if 'baths' in request.GET and request.GET['baths'] != '':
            housing = housing.filter(bath=request.GET['baths'])
        if 'price_min' in request.GET and request.GET['price_min'] != '':
            housing = housing.filter(rent__gte=int(request.GET['price_min']))
        if 'price_max' in request.GET and request.GET['price_max'] != '':
            housing = housing.filter(rent__lte=int(request.GET['price_max']))

        filters = request.GET
    else:
        filters = {'title': '', 'beds': '', 'baths': '', 'price_min': '', 'price_max': ''}

    context = {
        'housing': housing,
        'filters': filters,
    }

    return render(request, 'oauth_app/home.html', context)


def unofficial(request):
    housing = Housing.objects.all().filter(official=False)

    if request.method == 'GET':
        if 'title' in request.GET and request.GET['title'] != '':
            housing = housing.filter(title__icontains=request.GET['title'])
        if 'beds' in request.GET and request.GET['beds'] != '':
            housing = housing.filter(bed=request.GET['beds'])
        if 'baths' in request.GET and request.GET['baths'] != '':
            housing = housing.filter(bath=request.GET['baths'])
        if 'price_min' in request.GET and request.GET['price_min'] != '':
            housing = housing.filter(rent__gte=int(request.GET['price_min']))
        if 'price_max' in request.GET and request.GET['price_max'] != '':
            housing = housing.filter(rent__lte=int(request.GET['price_max']))

        filters = request.GET
    else:
        filters = {'title': '', 'beds': '', 'baths': '', 'price_min': '', 'price_max': ''}

    context = {
        'housing': housing,
        'filters': filters,
    }
    print("all done")
    return render(request, "oauth_app/unofficial.html", context)


def HousingForm(request):
    if request.method == 'POST':
        form = SubmitHousing(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SubmitHousing()

    return render(request, 'oauth_app/submit.html', {'form': form})


def Housing_Detail(request, housing_id):
    housing = get_object_or_404(Housing, pk=housing_id)
    housings = Housing.objects.all()
    housings_official = housings.filter(official=True)
    housings_unofficial = housings.filter(official=False)

    post = get_object_or_404(Housing, id = housing_id)
    fav = False
    if post.favorites.filter(id = request.user.id).exists():
        fav = True
    print(fav)
    
    if housing in housings_official:
        housings = housings_official
    else:
        housings = housings_unofficial
    num_surveys = housing.num_ratings
    try:
        num_star = int(housing.rating/housing.num_ratings)
    except ZeroDivisionError:
        num_star = 0
    ls_orange_star = [num for num in range(num_star)]
    ls_grey_star = [num for num in range(5 - num_star)]

    
    origin = "Toronto" # ADD ORIGIN ADDRESS (Rotunda)
    dest = "Montreal" # ADD DESTINATION ADDRESS (Current Listing's Address)

    link = 'https://maps.googleapis.com/maps/api/directions/json?origin='+origin+'&destination='+dest+'&key=AIzaSyCysBjLqjb5cKlZOAXhbIfB1PNgHWjSRGM'

    try:
        r = requests.get(link).json()
        duration = r['routes'][0]['legs'][0]['duration']['text']
        distance = r['routes'][0]['legs'][0]['distance']['text']
        call = True
        print('success')
    except:
        duration = ""
        distance = ""
        call = False


    return render(request, 'oauth_app/housing_detail.html', {'housing': housing, 'housings': housings, "grey_star":
        ls_grey_star, "orange_star": ls_orange_star, "num_surveys": num_surveys, 'fav':fav, 'duration' : duration,
        'distance' : distance, 'call' : call, })



def popularity(request, housing_id):
    housing = get_object_or_404(Housing, pk=housing_id)
    housings = Housing.objects.all()
    housings_official = housings.filter(official=True)
    housings_unofficial = housings.filter(official=False)
    if housing in housings_official:
        housings = housings_official
    else:
        housings = housings_unofficial
    try:

        user_evaluation = int(request.POST['eval'])
        housing.popularity += user_evaluation - 3
        housing.rating = housing.rating + user_evaluation
        housing.num_ratings += 1
        housing.save()
        return HttpResponseRedirect(reverse('oauth_app:housing_detail', args=(housing.id,)))
    except MultiValueDictKeyError:
        return HttpResponseRedirect(reverse('oauth_app:housing_detail', args=(housing.id,)))

"    ls_orange_star = [num for num in range(housing.average_rating)]                                                                                              "
"    ls_grey_star = [num for num in range(5 - housing.average_rating)]                                                                                            "
"    return render(request, 'oauth_app/housing_detail.html', {'housing': housing, 'housings': housings, 'grey_star': ls_grey_star, 'orange_star': ls_orange_star})"


@login_required(login_url='oauth_app:login')
def fav_add(request, housing_id):
    post = get_object_or_404(Housing, id=housing_id)
    print(request.user)
    if post.favorites.filter(id=request.user.id).exists():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='oauth_app:login')
def favorites(request):

    new = Housing.objects.filter(favorites=request.user)
    return render(request, "oauth_app/fav.html", {'new': new})


@login_required(login_url='oauth_app:login')
def profile(request):
    print(request.user.email)
    return render(request, "oauth_app/profile.html", {})

