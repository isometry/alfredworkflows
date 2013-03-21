#-*- coding: utf-8 -*-
# trailer.alfredworkflow, v0.1
# Robin Breathe, 2013

import alfred
try:
    import requests
except ImportError:
    import sys
    sys.path.append('./requests-1.1.0-py2.7.egg')
    import requests

from os import path
from time import time

_MAX_RESULTS = 9
SEARCH_TIMEOUT = 1.0
POSTER_TIMEOUT = 0.2
_BASE_URL = u'http://trailers.apple.com'
_QUICKFIND = u'/trailers/home/scripts/quickfind.php'
_JUSTADDED = u'/trailers/home/feeds/just_added.json'

def fetch_quickfind(query):
    r = requests.get(u''.join((_BASE_URL, _QUICKFIND)), params={'q': query}, timeout=SEARCH_TIMEOUT)
    if r.status_code != 200:
        return
    return r.json()

def fetch_justadded():
    r = requests.get(u''.join((_BASE_URL, _JUSTADDED)), timeout=SEARCH_TIMEOUT)
    if r.status_code != 200:
        return
    return r.json()

def fetch_poster(poster_uri):
    poster_name = u'_%s.%s' % (
        u'_'.join(poster_uri.split('/')[4:6]),
        poster_uri.split('.')[-1]
    )
    cache = path.join(alfred.work(volatile=True), poster_name)
    if path.isfile(cache):
        return cache
    try:
        r = requests.get(poster_uri, timeout=POSTER_TIMEOUT)
    except requests.exceptions.Timeout:
        return 'icon.png'
    if r.status_code != 200 or not r.headers['Content-Type'].startswith('image/'):
        return 'icon.png'
    with open(cache, 'wb') as cache_file:
        cache_file.write(r.content)
    return cache

def search_results(query, maxresults=_MAX_RESULTS):
    response = fetch_quickfind(query)

    if not response or response['error']:
        return alfred.xml([alfred.Item(
            attributes = {'uid': u'trailer://404', 'valid': u'no'},
            title = u'404 Trailer Not Found',
            subtitle = u'Sorry, the iTunes Movie Trailers server returned an error',
            icon = u'icon.png'
        )])

    results = []
    for r in response['results'][:maxresults]:
        address = u''.join((_BASE_URL, r['location']))
        results.append(alfred.Item(
            attributes = {'uid': u'trailer://%s' % r['location'], 'arg': address, 'autocomplete': r['title']},
            title = r['title'],
            subtitle = u'Rating: %(rating)s; Studio: %(studio)s' % r,
            icon = fetch_poster(u''.join((_BASE_URL, r['poster'])))
        ))

    # no matches
    if results == []:
        results.append(alfred.Item(
            attributes = {'uid': u'trailer://404', 'valid': u'no'},
            title = u'404 Trailer Not Found',
            subtitle = u'No trailers matching the query were found',
            icon = u'icon.png'
        ))

    return results

def latest_results(maxresults=_MAX_RESULTS):
    response = fetch_justadded()
    
    if not response:
        return alfred.xml([alfred.Item(
            attributes = {'uid': u'trailer://404', 'valid': u'no'},
            title = u'404 Latest Movies Not Found',
            subtitle = u'Sorry, the iTunes Movie Trailers server isn\'t responding',
            icon = u'icon.png'
        )])
    
    results = []
    for r in response[:maxresults]:
        address = u''.join((_BASE_URL, r['location']))
        results.append(alfred.Item(
            attributes = {'uid': u'trailer://%s' % r['location'], 'arg': address, 'autocomplete': r['title']},
            title = r['title'],
            subtitle = u'Studio: %(studio)s' % r,
            icon = fetch_poster(r['poster'])
        ))

    return results

def complete(query, maxresults=_MAX_RESULTS):
    if query == 'latest':
        results = latest_results()
    else:
        results = search_results(query)

    return alfred.xml(results, maxresults=_MAX_RESULTS)