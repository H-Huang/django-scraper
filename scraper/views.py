from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from scraper import scrapefunction
import json

# Create your views here.
def index(request, urls=None):
    print("In index view")
    return render(request, 'scraper/index.html', {"urls": urls })

def output(request):
    print("In output view")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        urls = body_unicode
        print("here are the urls:")
        scraped_data = scrapefunction.scrape(urls)
        return HttpResponse(
           scraped_data,
           content_type="application/json"
        )
