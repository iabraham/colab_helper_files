import numpy as np
import requests


def gaussian(x, mu, b=0, k=1):
    """Evaluate a unit variance gaussian with mean k*mu with 
       random noise b*rand()

    Parameters
    ----------
    x
        Plotting or evaluation variable
    mu
        Fundamental mean value
    b
        Spread of random noise around the mean value
    k
        Higher offsets of mean value
    """
    randval = np.random.rand()
    return (mu, b, k, randval), np.exp(-(x-mu*k+b*randval)**2/2)


def sensed_gaussian(x, params, dist):
    """Evaluate a unit variance gaussian with mean k*mu with 
       random noise b*rand()

    Parameters
    ----------
    params
        A tuple consisting of mu, b, k from the gaussian method that generated
        the pulse
    dist
        Distance of the sensor node from source node
    """
    mu, b, k, randval = params
    return np.exp(-(x-dist-mu*k+b*randval)**2/2)


def find_nearest(array, value):
    """ Find the element in 1-D array that is closest to value.

    Parameters
    ----------
    array
        A 1-D numpy array 
    value
        The value to look for in array
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def flatten(regular_list):
    """ Flattens a list using list comprehensions. 
    
    Parameters
    ----------
    regular_list:
        A singly nested list to flatten.
    """
    return [item for sublist in regular_list for item in sublist]


def download_file_from_google_drive(id, destination):
    """ Download a drive from Google Drive give id from shareable link. 
    
    Parameters
    ----------
    id:
        The file identifier from a shareable link
    destination:
        The filename to save as on local disk
    """
    
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    """ Function to filter out some Cookie business from Google and
        extract the actual data
    
    Parameters
    ----------
    response:
        The return value from a requests GET request
    """
    
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    """ Function to open write the proper response content from a 
        requests GET response to local disk.
        
    Parameters
    ----------
    response:
        The filtered return value from a requests GET request
    destination:
        A filename or file object denoting where to save file on
        local disk
    """
    
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
