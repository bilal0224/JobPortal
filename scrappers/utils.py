import requests
from enum import Enum
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException, HTTPError as HTTPErrorRequests

def simple_connector(url, headers=False):
    """Connects to a URL

    Args:
        url (String): URL to be connected to

    Raises:
        SystemExit: Exceptions based on the connection

    Returns:
        String: HTML
    """
    try:
        if headers:
            html = requests.get(url, headers=headers)
        else:
            html = requests.get(url)
        html.raise_for_status()
    except HTTPErrorRequests as e:
        print('HTTP ERROR')
        if (e.response.status_code == 403):
            html = requests.get(url, headers=headers)
            return html
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
        print('\nURL Connected: ', url, '\n')
        return html.text


class Status(Enum):
    FAILURE = 0
    OK = 1
    NEXT = 2

class HEADERS:
    header_one = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

def href_formatter(link):
    """
        1. If link startswith https:// or http://, remove the trailing slash.
        2. If link is an internal href, append a slash to both sides of the link.
    """
    if link.startswith('https://') or link.startswith('http://'):
        return link
    elif link[0] == '/' and link[-1] == '/':
        return link
    elif link[0] != '/' and link[-1] == '/':
        return '/' + link
    elif link[0] == '/' and link[-1] != '/':
        return link + '/'
    else:
        return '/' + link + '/'



