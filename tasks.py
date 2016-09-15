from __future__ import absolute_import
import os
import requests

from urllib.parse import urljoin

from bs4 import BeautifulSoup
from celeryapp import app


USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'


@app.task
def song_links():
    page = requests.get(
        'http://www.azlyrics.com/t/taylorswift.html',
        headers={'user-agent': USER_AGENT})
    parsed_content = BeautifulSoup(page.content, 'html.parser')
    links = parsed_content.find(id='listAlbum').find_all('a', href=True)
    for i, link in enumerate(links):
        href = link.get('href')
        title = link.text
        url = urljoin('http://www.azlyrics.com/lyrics/taylorswift.html', href)
        song_lyrics.apply_async(
            kwargs={'url': url, 'title': title}, countdown=i // 4)


OUTPUT_DIR = os.path.join(os.dirname(__file__), 'results')


@app.task
def song_lyrics(url, title):
    page = requests.get(url, headers={'user-agent': USER_AGENT})
    content = page.text.replace('<br>', '').encode('utf-8')
    parsed_content = BeautifulSoup(content, 'html.parser')
    ringtone = parsed_content.find('div', {'class': 'ringtone'})
    lyrics = ringtone.find_next_sibling('div').text
    filename = os.path.join(OUTPUT_DIR, '{}.txt'.format(title))
    with open(filename, 'w') as lyric_file:
        lyric_file.write(lyrics)
