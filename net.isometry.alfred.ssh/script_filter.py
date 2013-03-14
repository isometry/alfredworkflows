# $Id$
# Robin Breathe, 2013

from os import path
import xml.etree.ElementTree as ET
import re

query = "{query}"

bonjour_timeout = 0.1

if '@' in query:
    (user, host) = query.split('@', 1)
else:
    host = query
    user = None

pattern = re.compile('.*?%s' % '.*?\b?'.join(list(host)), flags=re.IGNORECASE)

arg = lambda u, h: u and '@'.join([u,h]) or h
uri = lambda u, h: 'ssh://%s' % arg(u, h)

def add_item(root, user, host):
    item = ET.SubElement(root, 'item', uid=uri(user, host), arg=arg(user, host))
    ET.SubElement(item, 'title').text = uri(user, host)
    ET.SubElement(item, 'subtitle').text = 'SSH to %s' % host
    ET.SubElement(item, 'icon', type='fileicon').text = '/Applications/Utilities/Terminal.app'

root = ET.Element('items')

# Add the default item: the original query
add_item(root, user, host)

hosts = set([])

try:
    with open(path.expanduser('~/.ssh/config'), 'r') as ssh_config:
        for line in (x for x in ssh_config if x.startswith('Host ')):
            for h in (x for x in line.split()[1:] if not ('*' in x or '?' in x or '!' in x)):
                hosts.add(h)
except IOError:
    pass

try:
    with open(path.expanduser('~/.ssh/known_hosts'), 'r') as known_hosts:
        for line in known_hosts:
            hosts.update(line.split()[0].split(','))
except IOError:
    pass

try:
    with open('/etc/hosts', 'r') as etc_hosts:
        for line in etc_hosts:
            if not line.startswith('#'):
                hosts.update(line.split()[1:])
except IOError:
    pass

try:
    from pybonjour import DNSServiceBrowse, DNSServiceProcessResult
    from select import select
    bj_callback = lambda s, f, i, e, n, t, d: hosts.add('%s.%s' % (n, d))
    bj_browser = DNSServiceBrowse(regtype = '_ssh._tcp', callBack = bj_callback)
    select([bj_browser], [], [], bonjour_timeout)
    DNSServiceProcessResult(bj_browser)
    bj_browser.close()
except ImportError:
    pass

hosts.discard(host)

for h in (h for h in hosts if pattern.match(h)):
    add_item(root, user, h)

print ET.tostring(root, encoding='utf-8')
