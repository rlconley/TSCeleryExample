from __future__ import absolute_import
import requests

from bs4 import BeautifulSoup
# from celery import app


# @app.task
def song_links():
    page = requests.get('http://www.azlyrics.com/t/taylorswift.html',
                        headers={'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    #have to mimic google bot here
    parsed_content = BeautifulSoup(page.content, 'html.parser')
    links = parsed_content.find_all('a')
    #this needs to exclude hrefs that aren't lyrics
    links_list = [link.get('href') for link in links]
    actual_links = [
        urljoin('http://www.azlyrics.com/lyrics/taylorswift.html', link) for link in links_list]
    return actual_links



