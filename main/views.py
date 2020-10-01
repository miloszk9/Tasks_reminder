from django.shortcuts import render

from django.http import HttpResponse # for test

def home(request):
    return HttpResponse('<h1>Test</h1>')
