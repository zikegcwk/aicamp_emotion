# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oJBq-Y646ru4hQJQxqjDY8sD1s2mDtWb
"""
import urllib.request

from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials
from requests import get

# pip install azure-cognitiveservices-search-imagesearch
# pip install requests
# comment

urllib.request.urlretrieve

search_term = input("What would you like to search?")
search_location = input("Where would you like to save? (Full Address Location)")

subscription_key = "97ec2cef9fd54460b3d2d43a987e3cac"
client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
image_results = client.images.search(query=search_term + '/')
i = 0


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


if image_results.value:
    while i < (len(image_results.value)):
        first_image_result = image_results.value[i]
        print("image", i + 1, "content url: {}".format(first_image_result.content_url))
        # urllib.request.urlretrieve("{}".format(first_image_result.content_url, "image {}".format(i)))
        download("{}".format(first_image_result.content_url), search_location + "image {}".format(i + 1))
        i = i + 1
else:
    print("No image results returned!")
