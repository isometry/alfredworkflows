# Open SSH.alfredworkflow, v0.10
# Robin Breathe, 2013

import alfred
from os import path
from time import time
import json
import re

class SSHItem(alfred.Item):
    def __init__(self, user, host):
        _arg = user and '@'.join([user,host]) or host
        _uri = 'ssh://%s' % _arg
        return super(SSHItem, self).__init__(attributes={'uid':_uri, 'arg':_arg},
            title=_uri, subtitle='SSH to %s' % host, icon='icon.png')

def fetch_ssh_config(_path):
    master = path.expanduser(_path)
    if path.isfile(master):
        cache = path.join(alfred.work(volatile=True), 'ssh_config.1.json')
        if path.isfile(cache) and path.getmtime(cache) > path.getmtime(master):
            return json.load(open(cache, 'r'))
        else:
            results = set([])
            try:
                with open(path.expanduser(_path), 'r') as ssh_config:
                    for line in (x for x in ssh_config if x.startswith('Host ')):
                        results.update((x for x in line.split()[1:] if not ('*' in x or '?' in x or '!' in x)))
            except IOError:
                pass
            json.dump(list(results), open(cache, 'w'))
            return results

def fetch_known_hosts(_path):
    master = path.expanduser(_path)
    if path.isfile(master):
        cache = path.join(alfred.work(volatile=True), 'known_hosts.1.json')
        if path.isfile(cache) and path.getmtime(cache) > path.getmtime(master):
            return json.load(open(cache, 'r'))
        else:
            results = set([])
            try:
                with open(path.expanduser(_path), 'r') as known_hosts:
                    for line in known_hosts:
                        results.update(line.split()[0].split(','))
            except IOError:
                pass
            json.dump(list(results), open(cache, 'w'))
            return results

def fetch_hosts(_path):
    master = path.expanduser(_path)
    if path.isfile(master):
        cache = path.join(alfred.work(volatile=True), 'hosts.1.json')
        if path.isfile(cache) and path.getmtime(cache) > path.getmtime(master):
            return json.load(open(cache, 'r'))
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
            return results

def fetch_bonjour(_service):
    cache = path.join(alfred.work(volatile=True), 'bonjour.1.json')
    if path.isfile(cache) and (time() - path.getmtime(cache) < 10):
        return json.load(open(cache, 'r'))
    else:
        results = set([])
        try:
            from pybonjour import DNSServiceBrowse, DNSServiceProcessResult
            from select import select
            bj_callback = lambda s, f, i, e, n, t, d: results.add('%s.%s' % (n, d))
            bj_browser = DNSServiceBrowse(regtype = _service, callBack = bj_callback)
            select([bj_browser], [], [], 0.1)
            DNSServiceProcessResult(bj_browser)
            bj_browser.close()
        except ImportError:
            pass
        json.dump(list(results), open(cache, 'w'))
        return results

def complete(query):
    if '@' in query:
        (user, host) = query.split('@', 1)
    else:
        (user, host) = (None, query)

    host_chars = map(lambda x: '\.' if x is '.' else x, list(host))
    pattern = re.compile('.*?%s' % '.*?\b?'.join(host_chars), flags=re.IGNORECASE)
    
    hosts = set([])
    hosts.update(fetch_ssh_config('~/.ssh/config'))
    hosts.update(fetch_known_hosts('~/.ssh/known_hosts'))
    hosts.update(fetch_hosts('/etc/hosts'))
    hosts.update(fetch_bonjour('_ssh._tcp'))
    hosts.discard(host)

    results = [SSHItem(user, host)]
    for host in (x for x in hosts if pattern.match(x)):
        results.append(SSHItem(user, host))

    return alfred.xml(results)
