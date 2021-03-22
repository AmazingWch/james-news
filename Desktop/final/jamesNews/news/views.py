import datetime
import json

import simplejson as simplejson
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
# from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from .models import Authors, Stories
from . import models
from .forms import StoriesForm
from django.http import HttpResponse


@csrf_exempt
def logIn(request):
    http_response = HttpResponse()
    http_response["Content-Type"] = 'text-plain'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User = models.User.objects.get(username=username)
        except:
            http_response.content = "no this user"
            http_response.status_code = 401
            return http_response

        # author0 = Authors.objects.filter(username=request.POST.get('username')).filter(password=request.POST.get('password'))
        user = authenticate(username=username, password=password)
        # print(author0)
        if user is None:
            http_response.status_code = 401
            http_response.content = 'authentication failed.'
        else:
            login(request, user)
            http_response.status_code = 200
            http_response.content = 'Welcome to the news world!'
        return http_response

    else:
        http_response.status_code = 405
        http_response.content = 'Only POST requests are allowed for this resource!'
        return http_response


@csrf_exempt
def logOut(request):
    http_response = HttpResponse()
    http_response['Content-Type'] = 'text/plain'

    if request.method == 'POST':
        if request.user.is_authenticated:
            http_response.status_code = 200
            http_response.content = 'Hope success follows you where you go, goodbye!'
            logout(request)
            return http_response

        else:
            http_response.status_code = 401
            http_response.content = 'Sorry, you are not logged in.'
            return http_response

    else:
        http_response.status_code = 405
        http_response.content = 'Only POST requests are allowed for this resource!'
        return http_response


@csrf_exempt
def postAStory(request):
    http_response = HttpResponse()
    http_response['Content-Type'] = "application/json"

    if request.method == 'POST':
        if request.user.is_authenticated:
            story = StoriesForm(simplejson.loads(request.body)).save(commit=False)
            story.author = request.user
            story.save()

            http_response.status_code = 201
            http_response.content = 'The new story is created.'
            return http_response
        else:
            http_response.status_code = 503
            http_response.content = 'Sorry, unauthenticated author.'
            return http_response
    else:
        http_response.status_code = 503
        http_response.content = 'Only POST requests are allowed for this resource!'
    return http_response


@csrf_exempt
def getStories(request):
    http_response = HttpResponse()

    if request.method == 'GET':
        find_data = dict()
        receive_data = simplejson.loads(request.body)

        if receive_data["story_cat"] != "*":
            find_data["category"] = receive_data["story_cat"]
        if receive_data["story_region"] != "*":
            find_data["region"] = receive_data["story_region"]
        if receive_data["story_date"] != "*":
            day, month, year = receive_data["story_date"].split('/')
            date = datetime.datetime(int(year), int(month), int(day))
            # after or on the given date
            find_data["date__gte"] = date

        stories = Stories.objects.all().filter(**find_data)

        if len(stories) == 0:
            http_response['Content-Type'] = 'text/plain'
            http_response.status_code = 404
            http_response.content = "Sorry, no stories are found."

        else:
            storiesList = [story.switchJson() for story in stories]
            response_data = {"stories": storiesList}

            http_response['Content-Type'] = "application/json"
            http_response.status_code = 200
            http_response.content = json.dumps(response_data)
        return http_response

    else:
        http_response.status_code = 405
        http_response.content = 'Only POST requests are allowed for this resource!'
        return http_response


@csrf_exempt
def deleteStory(request):
    http_response = HttpResponse()
    http_response['Content-Type'] = "application/json"

    if request.method == 'POST':
        if request.user.is_authenticated:
            key = int(simplejson.loads(request.body)["story_key"])
            try:
                story = Stories.objects.get(key=key)
            except story.DoesNotExist:
                http_response.status_code = 503
                http_response.content = "This story does not exist."
                return http_response
            story.delete()
            http_response.status_code = 201
            http_response.content = "This story is deleted."
            return http_response
        else:
            http_response.status_code = 503
            http_response.content = 'Sorry, unauthenticated author.'
            return http_response
    else:
        http_response.status_code = 503
        http_response.content = 'Only POST requests are allowed for this resource!'
    return http_response
