#-*- coding: utf-8 -*-
# pipe.alfredworkflow, v1.0
# Robin Breathe, 2013

import alfred
import json

from fnmatch import fnmatch
from os import path
from time import strftime

_MAX_RESULTS=9
_ALIASES_FILE=u'aliases.json'
_BUILTINS_FILE=u'builtins.json'
_TIMESTAMP=u'%Y-%m-%d @ %H:%M'

def fetch_aliases(_path=_ALIASES_FILE):
    file = path.join(alfred.work(volatile=False), _path)
    if not path.isfile(file):
        return {}
    return json.load(open(file, 'r'))

def write_aliases(_dict, _path=_ALIASES_FILE):
    file = path.join(alfred.work(volatile=False), _path)
    json.dump(_dict, open(file, 'w'), indent=4, separators=(',', ': '))

def define_alias(_dict, definition):
    if u'=' in definition:
        (alias, pipe) = definition.split(u'=', 1)
    else:
        (alias, pipe) = (definition, u'')

    if not alias:
        return alfred.xml([alfred.Item(
            attributes = {'uid': u'pipe:help', 'valid': u'no'},
            title = u"alias NAME=VALUE",
            subtitle = u'Terminate VALUE with @@ to save',
            icon = u'icon.png'
        )])

    if pipe and pipe.endswith('@@'):
        pipe = pipe[:-2]
        _dict[alias] = pipe
        write_aliases(_dict)
        return alfred.xml([alfred.Item(
            attributes = {'uid': u'pipe:{}'.format(pipe) , 'valid': u'no', 'autocomplete': alias},
            title = u"alias {}={}".format(alias, pipe),
            subtitle = u'Alias saved! TAB to continue',
            icon = u'icon.png'
        )])
    
    return alfred.xml([alfred.Item(
        attributes = {'uid': u'pipe:{}'.format(pipe) , 'valid': u'no'},
        title = u"alias {}={}".format(alias, pipe or 'VALUE'),
        subtitle = u'Terminate with @@ to save',
        icon = u'icon.png'
    )])

def exact_alias(_dict, query):
    pipe = _dict[query]
    return alfred.xml([alfred.Item(
        attributes = {'uid': u'pipe:{}'.format(pipe), 'arg': pipe},
        title = pipe,
        subtitle = u'(expanded alias)',
        icon = u'icon.png'
    )])

def match_aliases(_dict, query):
    results = []
    for (alias, pipe) in _dict.iteritems():
        if (pipe != query) and fnmatch(alias, u'{}*'.format(query)):
            results.append(alfred.Item(
                attributes = {'uid': u'pipe:{}'.format(pipe) , 'arg': pipe, 'autocomplete': pipe},
                title = pipe,
                subtitle = u'(alias: {})'.format(alias),
                icon = u'icon.png'
            ))
    return results

def fetch_builtins(_path=_BUILTINS_FILE):
    return json.load(open(_path, 'r'))

def match_builtins(_dict, query):
    results = []
    for (pipe, desc) in _dict.iteritems():
        if fnmatch(pipe, u'*{}*'.format(query)) or fnmatch(desc, u'*{}*'.format(query)):
            results.append(alfred.Item(
                attributes = {'uid': u'pipe:{}'.format(pipe) , 'arg': pipe, 'autocomplete': pipe},
                title = pipe,
                subtitle = u'(builtin: {})'.format(desc),
                icon = u'icon.png'
            ))
    return results

def verbatim(query):
    return alfred.Item(
        attributes = {'uid': u'pipe:{}'.format(query), 'arg': query},
        title = query,
        subtitle = None,
        icon = u'icon.png'
    )

def complete(query, maxresults=_MAX_RESULTS):
    aliases = fetch_aliases()
    builtins = fetch_builtins()

    if query.startswith('alias '):
        return define_alias(aliases, query[6:])

    results = []

    if query not in builtins:
        results.append(verbatim(query))

    for matches in (
        match_aliases(aliases, query),
        match_builtins(builtins, query)
    ):
        results.extend(matches)

    return alfred.xml(results, maxresults=maxresults)
