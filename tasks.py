from __future__ import absolute_import
import os
import requests

from urllib.parse import urljoin

from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger
from celeryapp import app


USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

logger = get_task_logger(__name__)


@app.task
def red(action='loving', color='red', description=''):
    message = '{action} him was {color}{description}.'.format(
                action=action.title(), color=color,
                description=' ' + description if description else '')
    logger.info(message)


@app.task
def song_links():
    page = requests.get(
        'http://www.songlyrics.com/taylor-swift-lyrics/',
        headers={'user-agent': USER_AGENT})
    parsed_content = BeautifulSoup(page.content, 'html.parser')
    links = parsed_content.find('div', {'id': 'colone-container'})
    links = links.find('table', {'class': 'tracklist'})
    links = links.find_all('a')
    for i, link in enumerate(links):
        href = link.get('href')
        title = link.text
        url = urljoin('http://www.azlyrics.com/lyrics/taylorswift.html', href)
        song_lyrics.apply_async(
            kwargs={'url': url, 'title': title}, countdown=i // 4)


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'results')



@app.task
def song_lyrics(url, title):
    page = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'})
    # have to mimic google bot here
    parsed_content = BeautifulSoup(page.content, 'html.parser')
    lyrics = parsed_content.find('p', {'id':'songLyricsDiv'}).text
    filename = os.path.join(OUTPUT_DIR, '{}.txt'.format(title))
    with open(filename, 'w') as lyric_file:
        lyric_file.write(lyrics)
