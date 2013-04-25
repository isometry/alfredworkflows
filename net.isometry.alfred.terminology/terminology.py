#-*- coding: utf-8 -*-
# terminology.alfredworkflow, v0.1
# Robin Breathe, 2013

import alfred
import json
import urllib2

from urllib import quote, urlencode
from os import path
from time import time

_MAX_RESULTS = 9
_TIMEOUT = 1.0
_BASE_URL = u'http://term.ly'
_MATCH_API = u'/api/matches.json'

def fetch_terms(query):
    req = urllib2.Request(u'%s?%s' % (u''.join((_BASE_URL, _MATCH_API)), urlencode({'q': query})))
    try:
        f = urllib2.urlopen(req, None, _TIMEOUT)
    except URLError:
        return []
    if f.getcode() != 200:
        return []
    return json.load(f)

def search_results(query, maxresults=_MAX_RESULTS):
    response = fetch_terms(query)

    results = []
    for r in response[:maxresults]:
        address = u'/'.join((_BASE_URL, quote(r)))
        results.append(alfred.Item(
            attributes = {'uid': address, 'arg': address, 'autocomplete': r},
            title = r,
            subtitle = u"Open %s on term.ly" % r,
            icon = u'icon.png'
        ))

    # no matches
    if results == []:
        results.append(alfred.Item(
            attributes = {'valid': u'no'},
            title = u'404 Term Not Found: %s' % query,
            subtitle = u"Sorry, term '%s' was not found on term.ly" % r,
            icon = u'icon.png'
        ))

    return results

def complete(query, maxresults=_MAX_RESULTS):
    results = search_results(query)

    return alfred.xml(results, maxresults=_MAX_RESULTS)

