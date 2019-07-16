import get
import requests
from requests import get
import pickle
import time


def download(url, file_name):
    '''
    function to download based on URL and file location
    url=url file_name=file location path
    '''
    # open in binary mode- write file
    with open(file_name, "wb") as file:
        # get request ask for the data from URL
        response = get(url)
        # write to file
        file.write(response.content)


def saveurl(search_terms, image_count, term):
    '''
    function to call Bing Images API to give URLs of images and to save them to a outfile
    search_terms=word being searched, image_count=# of images, term=type of image (happy, sad, etc)
    '''
    #Bing Images API Information for URL
    for val in search_terms:
        subscription_key = "89606185ba57483ab3952f85df1b39bb"
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        params = {
            "q": val,
            # +define the term for offset
            "offset": 0,
            "imageType": "photo",
            'minHeight': 100,
            'minWidth': 100,
            # +using count_step to determine # of URLs instead of range
            'count': image_count,
            'market': 'en-us'
        }
        #Variables and calculation for offsets (150 max images, 35 per page)
        base = int(image_count/150)
        z = 0
        a = 0
        listurl = []
        #Requests for ContentURL, loop to capture each URL
        #res=response, search_results=list/dictionary of info, url=one captured URL, listurl=stored URLS from the search_terms
        while z < base:
            params.update({'offset': a})
            res = requests.get("https://api.cognitive.microsoft.com/bing/v7.0/images/search?q=", headers=headers, params=params)
            search_results = res.json()
            i=0
            if search_results.get('value'):
                while i < len(search_results['value']):
                    url = search_results['value'][i]['contentUrl']
                    listurl.append(url)
                    print("adding url:" + url)
                    i=i+1
                    a=a+1
                z = z + 1
                a = int(a / 150) * 150
            #returns if there is no value in dictionary
            else:
                image_count == z
                return
            '''
            looks for outfile, if none exists one is created
            the list of urls is then appended to the old list of urls (if one exists)
            prevlisturl=urls stored in the outfile, listurl=current url list
            '''
            try:
                with open('outfile{}'.format(term), 'rb') as fp:
                    prevlisturl = pickle.load(fp)
                    prevlisturl.append(listurl)
                    prevlisturl= set(prevlisturl)
                    pickle.dump(prevlisturl, fp)
            except:
                with open('outfile{}'.format(term), 'wb') as fp:
                    pickle.dump(listurl, fp)


def downloadlist(term, file_name, search_location):
    '''
    downloads the list stored in the outfile, removes duplicate urls as well
    file_name=name to call images, search_location= save location path
    '''
    # do the try and search
    with open ('outfile{}'.format(term), 'rb') as fp:
        downloadurls = pickle.load(fp)
    n=1
    downloadurls= set(downloadurls)
    total=len(downloadurls)
    try:
        for val in downloadurls:
            try:
                download("{}".format(val), search_location + "/" + file_name + "{}".format(n) + ".png")
                print("currently downloading:{} out of {}".format(n, total))
                n=n+1
            except:
                print("Image downloaded is invalid or cannot be reached (internet), continuing with next image after a delay.")
                n=n+1
                time.sleep(480)
                continue
    except:
        print("The folder location does not exist or the reference command failed. Please create a folder (case sensitive) or do a search.")


def checklist(term):
    '''
    checks total amount of images stored to see if more needs to be downloaded
    term=outfile+term, or type of image (happy, sad, etc.)
    '''
    with open ('outfile{}'.format(term), 'rb') as fp:
        downloadurls = pickle.load(fp)
    downloadurls = set(downloadurls)
    total = len(downloadurls)
    print(total)


if __name__ == '__main__':
    #Before running, add subscription key!

    #To save the urls
    #input search words
    #search_terms = ['happy boy', 'smiling person']
    #iput amount of images to search
    #image_count = 540
    #input TYPE of image searched (happy, sad, etc).
    #term = "happy"
    #saveurl(search_terms, image_count, term)

    #To download the urls
    #input the TYPE of image searched
    #term = "happy"
    #input the name of the file (will name by file_name(1, 2, etc)
    #file_name = "happy people"
    #input where you want to save the file (for WINDOWS please add "r" BEFORE the search location, etc r"C:/Users/..."
    #search_location = r"C:\Users\Banana\Google Drive\Test"
    #downloadlist(term, file_name, search_location)

    #To check how many images are downloaded
    #input the TYPE of image searched
    #term = "happy"
    #checklist(term)
