"""The module to let beginners in Python studies it more easily.

This module is to visit a website with a URL.
Functions can return HTML file or files.

To use more, please install package "beginner-web".

Import the module and call it."""

import requests


def get_html(url: str, get_args=None, files=None) -> str:
    """:parameter url: The URL of a website.
    :parameter get_args: Args of GET request.
    :param files: Files of GET request.
    :return: HTML page (str type).
    Create a GET request and send to the website.
    The function returns the HTML text of the page.
    WARNING: IT DOES NOT RETURN JAVASCRIPT, CSS, XML OR OTHER FILES IN THE PAGE."""
    if files is None:
        files = {}
    if get_args is None:
        get_args = {}
    obj = requests.get(url=url, params=get_args, files=files)
    if not obj.ok:
        raise WebsiteVisitingFailedError(url=url, status_code=obj.status_code)  # Cannot visit the website.
    return str(obj.text, encoding=obj.encoding)


class WebsiteVisitingFailedError(Exception):
    """Cannot visit the website."""

    def __init__(self, url, status_code):
        """Define args in CLS."""
        self.url = url
        self.status_code = status_code

    def __str__(self):
        return "Cannot visit the website: {}. The HTTP/HTTPS status code: {}".format(self.url, self.status_code)


def post_url(url: str, **data):
    """:param url: The URL of a website.
    :param data: Default args of POST request.
    Send a POST request to a website page.
    :return: Response (dict type) from the website page."""
    res = requests.post(url, data)
    return res.text


def response(url: str, **options):
    try:
        res = requests.get(url, options)
    except Exception:
        raise WebsiteVisitingFailedError(url, 'None')
    else:
        return res
