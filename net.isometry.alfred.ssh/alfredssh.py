#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# ssh.alfredworkflow, v2.0
# Robin Breathe, 2013-2016

from __future__ import unicode_literals
from __future__ import print_function

import json
import re
import sys
import os

from time import time

DEFAULT_MAX_RESULTS=36

class Hosts(object):
    def __init__(self, original, user=None):
        self.original = original
        self.hosts = {original: ['input']}
        self.user = user

    def add(self, host, source):
        if host in self.hosts:
            self.hosts[host].append(source)
        else:
            self.hosts[host] = [source]

    def update(self, _list):
        if not _list:
            return
        (hosts, source) = _list
        for host in hosts:
            self.add(host, source)

    def item(self, host, source):
        _arg = self.user and '@'.join([self.user, host]) or host
        _uri = 'ssh://{}'.format(_arg)
        _sub = 'source: {}'.format(', '.join(source))
        return {
            "uid": _uri,
            "title": _uri,
            "subtitle": _sub,
            "arg": _arg,
            "icon": { "path": "icon.png" },
            "autocomplete": _arg
        }

    def json(self, _filter=(lambda x: True), maxresults=DEFAULT_MAX_RESULTS):
        items = [self.item(host=self.original, source=self.hosts[self.original])]
        for (host, source) in (
            (x, y) for (x, y) in self.hosts.items()
            if ((x != self.original) and _filter(x))
        ):
            items.append(self.item(host, source))
        return json.dumps({"items": items[:maxresults]})

def _create(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.access(path, os.W_OK):
        raise IOError('No write access: %s' % path)
    return path


def work(volatile):
    path = {
        True: os.getenv('alfred_workflow_cache'),
        False: os.getenv('alfred_workflow_data')
    }[bool(volatile)]
    if path is None:
        path = os.getenv('TMPDIR')
    return _create(os.path.expanduser(path))


def fetch_file(file_path, cache_prefix, parser, env_flag):
    """
    Parse and cache a file with the named parser
    """
    # Allow default sources to be disabled
    if env_flag is not None and int(os.getenv('alfredssh_{}'.format(env_flag), 1)) != 1:
        return

    # Expand the specified file path
    master = os.path.expanduser(file_path)

    # Skip a missing file
    if not os.path.isfile(master):
        return

    # Read from JSON cache if it's up-to-date
    if cache_prefix is not None:
        cache = os.path.join(work(volatile=True),
                          '{}.1.json'.format(cache_prefix))
        if os.path.isfile(cache) and os.path.getmtime(cache) > os.path.getmtime(master):
            return (json.load(open(cache, 'r')), file_path)

    # Open and parse the file
    try:
        with open(master, 'r') as f:
            results = parse_file(f, parser)
    except IOError:
        pass
    else:
        # Update the JSON cache
        if cache_prefix is not None:
            json.dump(list(results), open(cache, 'w'))
        # Return results
        return (results, file_path)

def parse_file(open_file, parser):
    parsers = {
        'ssh_config':
            (
                host for line in open_file
                if line[:5].lower() == 'host '
                for host in line.split()[1:]
                if not ('*' in host or '?' in host or '!' in host)
            ),
        'known_hosts':
            (
                host for line in open_file
                if line.strip() and not line.startswith('|')
                for host in line.split()[0].split(',')
            ),
        'hosts':
            (
                host for line in open_file
                if not line.startswith('#')
                for host in line.split()[1:]
                if host != 'broadcasthost'
            ),
        'extra_file':
            (
                host for line in open_file
                if not line.startswith('#')
                for host in line.split()
            )
    }
    results = set()
    results.update(parsers[parser])
    return results

def fetch_bonjour(_service, alias='Bonjour', timeout=0.1):
    if int(os.getenv('alfredssh_bonjour', 1)) != 1:
        return
    cache = os.path.join(work(volatile=True), 'bonjour.1.json')
    if os.path.isfile(cache) and (time() - os.path.getmtime(cache) < 60):
        return (json.load(open(cache, 'r')), alias)
    results = set()
    try:
        from pybonjour import DNSServiceBrowse, DNSServiceProcessResult
        from select import select
        bj_callback = lambda s, f, i, e, n, t, d: results.add('{}.{}'.format(n.lower(), d[:-1]))
        bj_browser = DNSServiceBrowse(regtype=_service, callBack=bj_callback)
        select([bj_browser], [], [], timeout)
        DNSServiceProcessResult(bj_browser)
        bj_browser.close()
    except ImportError:
        pass
    json.dump(list(results), open(cache, 'w'))
    return (results, alias)

def complete():
    query = sys.argv[1]
    maxresults = int(os.getenv('alfredssh_max_results', DEFAULT_MAX_RESULTS))

    if '@' in query:
        (user, host) = query.split('@', 1)
    else:
        (user, host) = (None, query)

    host_chars = (('\\.' if x is '.' else x) for x in list(host))
    pattern = re.compile('.*?\b?'.join(host_chars), flags=re.IGNORECASE)

    hosts = Hosts(original=host, user=user)

    for results in (
        fetch_file('~/.ssh/config', 'ssh_config', 'ssh_config', 'ssh_config'),
        fetch_file('~/.ssh/known_hosts', 'known_hosts', 'known_hosts', 'known_hosts'),
        fetch_file('/etc/hosts', 'hosts', 'hosts', 'hosts'),
        fetch_bonjour('_ssh._tcp')
    ):
        hosts.update(results)

    extra_files = os.getenv('alfredssh_extra_files')
    if extra_files:
        for file_spec in extra_files.split():
            (file_prefix, file_path) = file_spec.split('=', 1)
            hosts.update(fetch_file(file_path, file_prefix, 'extra_file', None))

    return hosts.json(pattern.search, maxresults=maxresults)

if __name__ == '__main__':
    print(complete())
