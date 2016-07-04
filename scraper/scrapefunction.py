"""This is a web scraper made for the Daily Bruin."""

from bs4 import BeautifulSoup
import requests
import json
import re

def scrape(urls):
    print("in scrape")
    urls = json.loads(urls)
    # print(urls)
    obj = []
    count = 1

    for url in urls:
        try:
            print("in loop")
            #print(url)
            r = requests.get(url)
            #print(r)
            soup = BeautifulSoup(r.content, "html.parser")

            #headline
            print("headline")
            headline = str(soup.find("div", class_="db-post-headline").text)
            authors = soup.find("div", class_="db-byline").find_all("a")
            tempList = []
            #getting authors
            for author in authors:
                tempList.append(str(author))
            #story
            story = soup.find("div", class_="db-post-content")
            story = str(story).split("\n<!-- Simple Share Buttons Adder")[0]
            story = story + "</div>"

            #changing the figures in story (TBD)

            dates = soup.find_all("h5")
            postingDate = ""
            #getting dates
            for date in dates:
                postingDate += str(date.text)
            regex1 = re.compile('.*wp-post-image.*')
            mainImage = soup.find("img", {"class": regex1})

            # trying to fetch image
            try:
                imageLink = str(mainImage).split("src=")[1]
                imageLink = re.sub(r'-\d\d\dx\d\d\d', '', imageLink)
                imageLink = imageLink.split("width=")[0][:-1]
                mainImage = imageLink[1:-1]
            except:
                mainImage = ""

            # trying to get title image caption
            try:
                imageCaption = str(soup.find(
                    "p", class_="db-image-caption").text).replace("\t", "").replace("\n", "")
            except:
                imageCaption = ""

            secondaryImages = []
            regex2 = re.compile('.*wp-image.*')
            images = soup.find_all("img", {"class": regex2})
            # trying to get secondary images
            try:
                for image in images:
                    imageLink = str(image).split("src=")[1]
                    imageLink = re.sub(r'-\d\d\dx\d\d\d', '', imageLink)
                    imageLink = imageLink.split("width=")[0][:-1][1:-1]
                    secondaryImages.append(imageLink)
            except:
                continue

            secondaryImageCaptions = []
            captions = soup.find_all("figcaption")
            # trying to get secondaryImageCaptions
            try:
                for caption in captions:
                    secondaryImageCaptions.append(caption.text)
            except:
                continue

            # APPEND EVERYTHING INTO THIS MASSIVE JSON OBJECT YAYAYYAAA
            obj.append({u"headline": headline, u"postDate": postingDate, u"authors": tempList, u"content": story,
                        u"titleImage": mainImage, u"titleCaption": imageCaption, u"url": url, u"secondaryImages": secondaryImages,
                        u"secondaryImageCaptions": secondaryImageCaptions})
            # If you want to see the JSON object outputted in terminal, uncomment the line below
            #print(json.dumps(obj, indent=4))

            print("URL number " + str(count) +
                  " scraped" + " (" + str(url) + ")")
            count += 1


        except requests.exceptions.RequestException as e:
            print(e)

    return json.dumps(obj, indent=4)
