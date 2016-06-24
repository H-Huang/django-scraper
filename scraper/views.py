from django.shortcuts import render
from django.http import HttpResponse
import scraper.scrapefunction
import json

# Create your views here.
def index(request):
    print("index")
    return render(request, 'scraper/index.html')

def output(request):
    print("output")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        urls = body_unicode
        print("here are the urls")
        print(urls)
        print("working?")
        scraped_data = scraper.scrapefunction.scrape(urls)
        return HttpResponse(
            scraped_data,
            content_type="application/json"
        )
