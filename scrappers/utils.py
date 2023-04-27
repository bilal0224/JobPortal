import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException, HTTPError as HTTPErrorRequests

def simple_connector(url):
    try:
        html = requests.get(url)
        html.raise_for_status()
    except HTTPErrorRequests as e:
        print('HTTP ERROR')
        return None
    except ConnectionError as e:
        print('CONNECTION ERROR')
        return None
    except Timeout as e:
        print('TIMEOUT')
        return None
    except TooManyRedirects as e:
        print('BAD URL: TOO MANY REDIRECTS')
        return None
    except RequestException as e:
        raise SystemExit(e)
    else:
        print('URL Connected: ', url)
        return html.text
