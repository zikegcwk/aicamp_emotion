import get
import requests
from requests import get
import os
import pickle
import ipdb
#sets function to create and write to file from the URL
def download(url, file_name):
    # open in binary mode- write file
    with open(file_name, "wb") as file:
        # get request ask for the data from URL
        response = get(url)
        # write to file
        file.write(response.content)
def saveurl():
    #used to save URLS
    term = input("What is the type of image (happy, sad, etc)? ")
    #input values for search
    search_term = input("What are you trying to search for? ")
    count_step = int(input("How many searches would you like? "))

    #set variables for the URL
    subscription_key = "97ec2cef9fd54460b3d2d43a987e3cac"
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    #use variables to store into parameters for URL
    params = {

        "q": search_term,
        # +define the term for offset
        "offset": 0,
        "license": "public",
        "imageType": "photo",
        'minHeight': 25,
        'minWidth': 25,
        # +using count_step to determine # of URLs instead of range
        'count': count_step,
        'market': 'en-us'

    }

    # sending info to Bing, converting results to extract and download URL
    #set variables (i=offset count or total URLs, url_prev=looking at previous URL to avoid duplicates
    i=0
    off= 0
    url_prev= ""
    listurl = []
    z=0
    #while loop to download URLs OF n to disregard duplicates
    while z < count_step:
        #updating offset to avoid same URL response
        params.update({'offset': off*35})
        #get request from API and store as response variable type
        res = requests.get("https://api.cognitive.microsoft.com/bing/v7.0/images/search?q=", headers=headers, params=params)
        #converting the response to a readable .json for the search_results variable (dictionary+lists)
        search_results = res.json()
        #extracting URL of the photo ONLY from the dictionaries+lists
        url = search_results['value'][z]['contentUrl']
        #ipdb.set_trace()
        print ("checking " + url)
        with open('outfile{}'.format(term), 'rb') as fp:
            listurl = pickle.load(fp)
        #prevent the duplicate URLs from previous URLs with console feedback (not necessary)
        listurl.append(url)
        listurl = list(dict.fromkeys(listurl))
        with open ('outfile{}'.format(term), 'wb') as fp:
            pickle.dump(listurl, fp)
        z = z+1
        print("current image: " + str(z))
        off=int(count_step/35)
        i=i+1


def downloadlist(term, search_term):
    # do the try and search
    search_location = input("Where would you like to save the pictures? ")
    with open ('outfile{}'.format(term), 'rb') as fp:
        listurl = pickle.load(fp)
    listurl = list(dict.fromkeys(listurl))
    n=1
    total=len(listurl)
    for val in listurl:
        download("{}".format(val), search_location + "/" + search_term + "{}".format(n) + ".png")
        print("currently downloading:{} out of {}".format(n, total))
        n=n+1

#ADD Function below


#//set
