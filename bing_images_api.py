import pickle
import time

import get
import requests
from requests import get


def download(url, file_name):
    """
    function to download based on URL and file location
    url=url file_name=file location path
    """
    # open in binary mode- write file
    with open(file_name, 'wb') as file:
        # get request ask for the data from URL
        response = get(url)
        # write to file
        file.write(response.content)


# function to call Bing Images API to give URLs of images and to save them to a outfile
# search_term=word being searched, image_count=# of images, term=type of image (happy, sad, etc)
def save_url(search_term, image_count, term):
    # Bing Images API Information for URL
    subscription_key = ''
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'q': search_term,
        # +define the term for offset
        'offset': 0,
        'license': 'public',
        'imageType': 'photo',
        'minHeight': 100,
        'minWidth': 100,
        # +using count_step to determine # of URLs instead of range
        'count': image_count,
        'market': 'en-us'
    }
    # Variables and calculation for offsets (150 max images, 35 per page)
    split = image_count / 150
    base = 1
    z = 0
    list_url = []
    # Requests for ContentURL, loop to capture each URL
    # res=response, search_results=list/dictionary of info, url=one captured URL, 
    # list_url=stored URLS from the search_term
    while z < split:
        params.update({'offset': z * 150})
        res = requests.get('https://api.cognitive.microsoft.com/bing/v7.0/images/search?q=', headers=headers,
                           params=params)
        search_results = res.json()
        i = 0
        while i < len(search_results['value']):
            url = search_results['value'][i]['contentUrl']
            list_url.append(url)
            print('adding url:' + url)
            i = i + 1
        z = z + 1
        # looks for outfile, if none exists one is created
        # the list of urls is then appended to the old list of urls (if one exists)
        # prev_list_url=urls stored in the outfile, list_url=current url list
        try:
            with open('outfile{}'.format(term), 'rb') as fp:
                prev_list_url = pickle.load(fp)
                prev_list_url.append(list_url)
                set(prev_list_url)
                pickle.dump(prev_list_url, fp)
        except OSError:
            with open('outfile{}'.format(term), 'wb') as fp:
                pickle.dump(list_url, fp)


# downloads the list stored in the outfile, removes duplicate urls as well
# file_name=name to call images, search_location= save location path
def download_list(term, file_name, search_location):
    # do the try and search
    with open('outfile{}'.format(term), 'rb') as fp:
        download_urls = pickle.load(fp)
    n = 1
    total = len(download_urls)
    try:
        for val in download_urls:
            try:
                download('{}'.format(val), search_location + '/' + file_name + '{}'.format(n) + '.png')
                print('currently downloading:{} out of {}'.format(n, total))
                n = n + 1
            except OSError:
                print(
                    'Image downloaded is invalid or cannot be reached (internet), '
                    'continuing with next image after a delay.')
                n = n + 1
                time.sleep(480)
                continue
    except OSError:
        print(
            'The folder location does not exist or the reference command failed. '
            'Please create a folder (case sensitive) or do a search.')


# checks total amount of images stored to see if more needs to be downloaded
# term=outfile+term, or type of image (happy, sad, etc.)
def checklist(term):
    with open('outfile{}'.format(term), 'rb') as fp:
        download_urls = pickle.load(fp)
    total = len(download_urls)
    print(total)

# write a function that takes a list of search terms and just save the images. 

# EXAMPLES OF FUNCTIONS
# save_url('deadpan person', 520, 'poker')
# save_url('unemotional person', 520, 'poker')
# save_url('unemotional face', 520, 'poker')
# save_url('straight face person', 520, 'poker')
# save_url('emotionless person', 520, 'poker')
# save_url('emotionless face', 520, 'poker')
# save_url('serious person', 520, 'poker')
# save_url('serious face', 520, 'poker')
# save_url('blank expression', 520, 'poker')
# download_list('poker', 'poker face', r'C:\Users\Thomas\Google Drive\Pycharm\BingAPI\poker')
# checklist('poker')
