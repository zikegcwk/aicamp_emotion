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


def save_url(search_terms, image_count, term):
    """
    function to call Bing Images API to give URLs of images and to save them to a outfile
    search_terms=word being searched, image_count=# of images, term=type of image (happy, sad, etc)
    """
    # Bing Images API Information for URL *Insert Subscription Key!*
    subscription_key = 'a10ac1d7aff040f1b56a360ceb821b4f'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    for val in search_terms:
        params = {
            'q': val,
            # +define the term for offset
            'offset': 0,
            'imageType': 'photo',
            'minHeight': 100,
            'minWidth': 100,
            # +using count_step to determine # of URLs instead of range
            'count': image_count,
            'market': 'en-us'
        }
        # Variables and calculation for offsets (150 max images, 35 per page)
        offset_times = int((image_count / 150) + 1)
        next_offset = 0
        list_url = []
        # Requests for ContentURL, loop to capture each URL res=response, search_results=list/dictionary of info,
        # url=one captured URL, list_url=stored URLS from the search_terms
        for timer in range(offset_times):  # AND search_number is less than totalEstimatedMatches
            params.update({'offset': next_offset})
            res = requests.get('https://api.cognitive.microsoft.com/bing/v7.0/images/search?q=', headers=headers,
                               params=params)
            search_results = res.json()
            if image_count > search_results.get('totalEstimatedMatches'):
                print('Error, too many images requested. Requested {} images, {} images exist'
                      .format(image_count, search_results.get('totalEstimatedMatches')))
                break
            else:
                if search_results.get('value'):
                    for search_number in (search_results['value']):
                        url = search_number['contentUrl']
                        list_url.append(url)
                        print('adding url:' + url)
                    next_offset = search_results.get('nextOffset')
                # returns if there is no value in dictionary
                else:
                    return
                '''
                looks for outfile, if none exists one is created
                the list of urls is then appended to the old list of urls (if one exists)
                prev_list_url=urls stored in the outfile, list_url=current url list
                '''
                try:
                    with open('output_file_{}'.format(term), 'rb') as fp:
                        prev_list_url = pickle.load(fp)
                        prev_list_url = prev_list_url + list_url
                        prev_list_url = list(set(prev_list_url))
                    with open('output_file_{}'.format(term), 'wb') as fp:
                        pickle.dump(prev_list_url, fp)
                except:  # TODO add specific error code
                    with open('output_file_{}'.format(term), 'wb') as fp:
                        pickle.dump(list_url, fp)


def download_list(term, file_name, search_location):
    """
    downloads the list stored in the outfile, removes duplicate urls as well
    file_name=name to call images, search_location= save location path
    """
    # do the try and search
    with open('output_file_{}'.format(term), 'rb') as fp:
        download_urls = pickle.load(fp)
    download_urls = set(download_urls)
    total = len(download_urls)
    try:
        for idx, val in enumerate(download_urls, start=1):
            try:
                download('{}'.format(val), search_location + '/' + file_name + '{}'.format(idx) + '.png')
                print('currently downloading:{} out of {}'.format(idx, total))
            except:  # TODO add specific error code
                print(
                    'Image downloaded is invalid or cannot be reached (internet), continuing with next image after a '
                    'delay.')
                time.sleep(10)
                continue
    except:  # TODO add specific error code
        print(
            'The folder location does not exist or the reference command failed. Please create a folder (case '
            'sensitive) or do a search.')


def checklist(term):
    """
    checks total amount of images stored to see if more needs to be downloaded
    term=outfile+term, or type of image (happy, sad, etc.)
    """
    with open('output_file_{}'.format(term), 'rb') as fp:
        download_urls = pickle.load(fp)
    download_urls = set(download_urls)
    total = len(download_urls)
    print(total)


if __name__ == '__main__':
    download()
    save_url()
    download_list()
    checklist()
# Before running, add subscription key!

# To save the urls
# input search words
# search_terms = ['happy person', 'smiling person']
# (Use multiples of 150 for searches etc 150, 300, 450) input amount of images to search
# image_count = 200
# input TYPE of image searched (happy, sad, etc).
# term = 'happy'
# save_url(search_terms, image_count, term)

# To download the urls
# input the TYPE of image searched
# term = 'happy'
# input the name of the file (will name by file_name(1, 2, etc)
# file_name = 'happy people'
# input where you want to save the file (for WINDOWS please add 'r' BEFORE the search location, etc r'C:/Users/...'
# search_location = r'C:\Banana\BingAPI\Test'
# download_list(term, file_name, search_location)

# To check how many images are downloaded
# input the TYPE of image searched
# term = 'happy'
# checklist(term)
