# Open SSH.alfredworkflow, v0.8
# Robin Breathe, 2013

from os import path
import xml.etree.ElementTree as ET
import re

query = "{query}"

bonjour_timeout = 0.1

if '@' in query:
    (user, host) = query.split('@', 1)
else:
    (user, host) = (None, query)

host_chars = map(lambda x: '\.' if x is '.' else x, list(host))
pattern = re.compile('.*?%s' % '.*?\b?'.join(host_chars), flags=re.IGNORECASE)

arg = lambda u, h: u and '@'.join([u,h]) or h

def add_item(root, user, host):
    _arg = arg(user, host)
    _uri = 'ssh://%s' % _arg
    item = ET.SubElement(root, 'item', uid=_uri, arg=_arg, autocomplete=_arg)
    ET.SubElement(item, 'title').text = _uri
    ET.SubElement(item, 'subtitle').text = 'SSH to %s' % host
    ET.SubElement(item, 'icon', type='fileicon').text = '/Applications/Utilities/Terminal.app'

def parse_ssh_config(_path):
    results = set([])
    try:
        with open(path.expanduser(_path), 'r') as ssh_config:
            for line in (x for x in ssh_config if x.startswith('Host ')):
                results.update((x for x in line.split()[1:] if not ('*' in x or '?' in x or '!' in x)))
    except IOError:
        pass
    return results

def parse_known_hosts(_path):
    results = set([])
    try:
        with open(path.expanduser(_path), 'r') as known_hosts:
            for line in known_hosts:
                results.update(line.split()[0].split(','))
    except IOError:
        pass
    return results

def parse_hosts(_path):
    results = set([])
    try:
        with open(_path, 'r') as etc_hosts:
            for line in (x for x in etc_hosts if not x.startswith('#')):
                results.update(line.split()[1:])
        results.discard('broadcasthost')
    except IOError:
        pass
    return results

def discover_bonjour(_service):
    results = set([])
    try:
        from pybonjour import DNSServiceBrowse, DNSServiceProcessResult
        from select import select
        bj_callback = lambda s, f, i, e, n, t, d: results.add('%s.%s' % (n, d))
        bj_browser = DNSServiceBrowse(regtype = _service, callBack = bj_callback)
        select([bj_browser], [], [], bonjour_timeout)
        DNSServiceProcessResult(bj_browser)
        bj_browser.close()
    except ImportError:
        pass
    return results

def discover_bonjour(_service):
    results = set([])
    from pybonjour import DNSServiceBrowse, DNSServiceProcessResult
    from select import select
    bj_callback = lambda s, f, i, e, n, t, d: results.add('%s.%s' % (n, d))
    bj_browser = DNSServiceBrowse(regtype = _service, callBack = bj_callback)
    select([bj_browser], [], [], bonjour_timeout)
    DNSServiceProcessResult(bj_browser)
    bj_browser.close()
    return results

hosts = set([])
hosts.update(parse_ssh_config('~/.ssh/config'))
hosts.update(parse_known_hosts('~/.ssh/known_hosts'))
hosts.update(parse_hosts('/etc/hosts'))
hosts.update(discover_bonjour('_ssh._tcp'))
hosts.discard(host)

root = ET.Element('items')
add_item(root, user, host)
for h in (h for h in hosts if pattern.match(h)):
    add_item(root, user, h)

print ET.tostring(root, encoding='utf-8')
