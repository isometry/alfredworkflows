# Open SSH.alfredworkflow, v1.0
# Robin Breathe, 2013

import alfred
from os import path
from time import time
import json
import re

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
        (hosts, source) = _list
        for host in hosts:
            self.add(host, source)
    
    def item(self, host, source):
        _arg = self.user and '@'.join([self.user,host]) or host
        _uri = 'ssh://%s' % _arg
        _sub = 'Connect to %s (source: %s)' % (_uri, ', '.join(source))
        return alfred.Item(attributes={'uid':_uri, 'arg':_arg, 'autocomplete':_arg},
            title=_uri, subtitle=_sub, icon='icon.png')
    
    def xml(self, _filter=(lambda x:True)):
        items = [self.item(host=self.original, source=self.hosts[self.original])]
        for (host, source) in ((x,y) for (x,y) in self.hosts.iteritems() if x<>self.original and _filter(x)):
            items.append(self.item(host, source))
        return alfred.xml(items)
    

def fetch_ssh_config(_path, alias='~/.ssh/ssh_config'):
    master = path.expanduser(_path)
    if path.isfile(master):
        cache = path.join(alfred.work(volatile=True), 'ssh_config.1.json')
        if path.isfile(cache) and path.getmtime(cache) > path.getmtime(master):
            return (json.load(open(cache, 'r')), alias)
        else:
            results = set([])
            try:
                with open(path.expanduser(_path), 'r') as ssh_config:
                    for line in (x for x in ssh_config if x.startswith('Host ')):
                        results.update((x for x in line.split()[1:] if not ('*' in x or '?' in x or '!' in x)))
            except IOError:
                pass
            json.dump(list(results), open(cache, 'w'))
            return (results, alias)

def fetch_known_hosts(_path, alias='~/.ssh/known_hosts'):
    master = path.expanduser(_path)
    if path.isfile(master):
        cache = path.join(alfred.work(volatile=True), 'known_hosts.1.json')
        if path.isfile(cache) and path.getmtime(cache) > path.getmtime(master):
            return (json.load(open(cache, 'r')), alias)
        else:
            results = set([])
            try:
                with open(path.expanduser(_path), 'r') as known_hosts:
                    for line in known_hosts:
                        results.update(line.split()[0].split(','))
            except IOError:
                pass
            json.dump(list(results), open(cache, 'w'))
            return (results, alias)

def fetch_hosts(_path, alias='/etc/hosts'):
    master = path.expanduser(_path)
    if path.isfile(master):
        cache = path.join(alfred.work(volatile=True), 'hosts.1.json')
        if path.isfile(cache) and path.getmtime(cache) > path.getmtime(master):
            return (json.load(open(cache, 'r')), alias)
        else:
            results = set([])
            try:
                with open(_path, 'r') as etc_hosts:
                    for line in (x for x in etc_hosts if not x.startswith('#')):
                        results.update(line.split()[1:])
                results.discard('broadcasthost')
            except IOError:
                pass
            json.dump(list(results), open(cache, 'w'))
            return (results, alias)

def fetch_bonjour(_service, alias='Bonjour', timeout=0.1):
    cache = path.join(alfred.work(volatile=True), 'bonjour.1.json')
    if path.isfile(cache) and (time() - path.getmtime(cache) < 60):
        return (json.load(open(cache, 'r')), alias)
    else:
        results = set([])
        try:
            from pybonjour import DNSServiceBrowse, DNSServiceProcessResult
            from select import select
            bj_callback = lambda s, f, i, e, n, t, d: results.add('%s.%s' % (n.lower(), d[:-1]))
            bj_browser = DNSServiceBrowse(regtype = _service, callBack = bj_callback)
            select([bj_browser], [], [], timeout)
            DNSServiceProcessResult(bj_browser)
            bj_browser.close()
        except ImportError:
            pass
        json.dump(list(results), open(cache, 'w'))
        return (results, alias)

def complete(query):
    if '@' in query:
        (user, host) = query.split('@', 1)
    else:
        (user, host) = (None, query)

    host_chars = map(lambda x: '\.' if x is '.' else x, list(host))
    pattern = re.compile('.*?\b?'.join(host_chars), flags=re.IGNORECASE)
    
    hosts = Hosts(original=host, user=user)
    hosts.update(fetch_ssh_config('~/.ssh/config'))
    hosts.update(fetch_known_hosts('~/.ssh/known_hosts'))
    hosts.update(fetch_hosts('/etc/hosts'))
    hosts.update(fetch_bonjour('_ssh._tcp'))

    return hosts.xml(pattern.search)
