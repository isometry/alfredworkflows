#-*- coding: utf-8 -*-
# pipe.alfredworkflow, v1.0
# Robin Breathe, 2013

import alfred
import json

from fnmatch import fnmatch
from os import path

_MAX_RESULTS=9
_ALIASES_FILE=u'aliases.json'
_BUILTINS_FILE=u'builtins.json'
_TIMESTAMP=u'%Y-%m-%d @ %H:%M'

def fetch_aliases(_path=_ALIASES_FILE):
    if not path.isfile(_path):
        return {}
    return json.load(open(_path, 'r'))

def update_aliases(_dict, _path=_ALIASES_FILE):
    json.dump(_dict, open(_path, 'w'))

def fetch_builtins(_path=_BUILTINS_FILE):
    return json.load(open(_path, 'r'))

def complete(query, maxresults=_MAX_RESULTS):
    aliases = fetch_aliases()
    builtins = fetch_builtins()

    if query.startswith('alias '):
        if query.endswith('$$'):
            (alias, pipe) = query[6:-2].split(u'=', 1) # XXX: this could error
            aliases[alias] = pipe
            update_aliases(aliases)
            return alfred.xml([alfred.Item(
                attributes = {'uid': u'pipe:{}'.format(pipe) , 'valid': u'no', 'autocomplete': alias},
                title = u"{} => ({})".format(alias, pipe),
                subtitle = u'Alias saved! Hit Enter to continue',
                icon = u'icon.png'
            )])
        if u' ' in query[6:]:
            (alias, pipe) = query[6:].split(u' ', 1)
        else:
            (alias, pipe) = (query[6:], u'')
        return alfred.xml([alfred.Item(
            attributes = {'uid': u'pipe:{}'.format(pipe) , 'valid': u'no'},
            title = u"Alias {} => ({})".format(alias, pipe),
            subtitle = u'Terminate one-liner with $$ and hit Enter to save',
            icon = u'icon.png'
        )])

    if query in aliases:
        pipe = aliases[query]
        return alfred.xml([alfred.Item(
            attributes = {'uid': u'pipe:{}'.format(pipe), 'arg': pipe},
            title = pipe,
            subtitle = u'(expanded alias)',
            icon = u'icon.png'
        )])

    results = [alfred.Item(
            attributes = {'uid': u'pipe:{}'.format(query) , 'arg': query},
            title = query,
            subtitle = None,
            icon = u'icon.png'
    )]
    for (alias, pipe) in aliases.iteritems():
        if fnmatch(alias, u'{}*'.format(query)):
            results.append(alfred.Item(
                attributes = {'uid': u'pipe:{}'.format(pipe) , 'arg': pipe, 'autocomplete': pipe},
                title = pipe,
                subtitle = u'(alias: {})'.format(alias),
                icon = u'icon.png'
            ))

    for (pipe, description) in builtins.iteritems():
        if fnmatch(pipe, u'*{}*'.format(query)):
            results.append(alfred.Item(
                attributes = {'uid': u'pipe:{}'.format(pipe) , 'arg': pipe, 'autocomplete': pipe},
                title = pipe,
                subtitle = u'(builtin: {})'.format(description),
                icon = u'icon.png'
            ))

    return alfred.xml(results, maxresults=maxresults)
