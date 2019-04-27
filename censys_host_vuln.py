import itertools

from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysNotFoundException

# via https://stackoverflow.com/a/8991553
def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

class Module(BaseModule):
    meta = {
        'name': 'Censys vulnerabilities by IP',
        'author': 'J Nazario',
        'description': 'Retrieves vulnerabilities identified by Censys for each IP address. Updates the \'vulnerabilities\' table with the results.',
        'query': 'SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL',
        'required_keys': ['censysio_id', 'censysio_secret'],
    }

    def module_run(self, hosts):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret)   
        IPV4_FIELDS = [ 'ip', 'protocols']
        VULN_FIELDS = [('443.https.ssl_3.support', 'Poodle'),
                       ('443.https.heartbleed.heartbleed_vulnerable', 'Heartbleed'),
                       ('443.https.heartbleed.heartbeat_enabled', 'Not Heartbleed'),
                       ('443.https.rsa_export.support', 'FREAK'), 
                       ('443.https.dhe_export.support', 'Logjam'), ]
        for ips in grouper(20, hosts):
            try:
                results = c.search(' OR '.join([ 'ip:{0}'.format(x) for x in ips ]), fields=IPV4_FIELDS + [ x for x,y in VULN_FIELDS ])
            except CensysException:
                continue
            for result in results:
                ip = result['ip']
                for k,t in VULN_FIELDS:
                    data = {'host': ip,
                            'category': 'TLS vulnerabilitity'}                            
                    if 'heartbleed' in k:
                        # just because heartbleed_vulnerable is True doesn't mean it
                        # if they have heartbleed_enabled, too. check for that
                        if result.get('443.https.heartbleed.heartbeat_enabled', False):
                            continue
                        elif result.get('443.https.heartbleed.heartbleed_vulnerable', False):
                            data['reference'] = 'VULNERABLE: Heartbleed'
                            self.add_vulnerabilities(**data)
                            continue
                    data['reference'] = 'VULNERABLE: {0}'.format(t)
                    self.add_vulnerabilities(**data)