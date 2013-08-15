from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
import datetime

# Create your views here.

def home(request):
    # return HttpResponse('blah blah blah')
    return render(request, 'project/home.html', {})
    # run the login template
    