from __future__ import absolute_import
import requests

from urllib.parse import urljoin

from bs4 import BeautifulSoup
from celeryapp import app


@app.task
def song_links():
    page = requests.get('http://www.azlyrics.com/t/taylorswift.html', headers={'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    # have to mimic google bot here
    parsed_content = BeautifulSoup(page.content, 'html.parser')
    links = parsed_content.find(id='listAlbum').find_all('a', href=True)
    for link in links:
        href = link.get('href')
        title = link.text
        url = urljoin('http://www.azlyrics.com/lyrics/taylorswift.html', href)
        song_lyrics.delay(url, title)

@app.task
def song_lyrics(url, title):
    page = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    # have to mimic google bot here
    parsed_content = BeautifulSoup(page.text.replace('<br>', '').encode('utf-8'), 'html.parser')
    # parent_div = parsed_content.find("div", {"class": "main-page"})
    lyrics = parsed_content.find('div', {'class': 'ringtone'}).find_next_sibling('div').text
    saved_lyrics = open("lyrics.txt", "w")
    saved_lyrics.write(title)
    saved_lyrics.write(lyrics)
    saved_lyrics.close()
