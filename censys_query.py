from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException

class Module(BaseModule):
    meta = {
        'name': 'Censys hosts by search terms',
        'author': 'J Nazario',
        'description': 'Retrieves details for hosts matching an arbitrary Censys query.  Updates the \'hosts\', \'domains\', and \'ports\' tables with the results.',
        'query': 'SELECT COUNT(DISTINCT(host)) FROM hosts WHERE host IS NOT NULL',
        'required_keys': ['censysio_id', 'censysio_secret'],   
        'options': (
            ('CENSYS_QUERY', '80.http.get.title: "Welcome to recon-ng"', True, 'the Censys query to execute'),
        )
    }

    def module_run(self, _):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        query = self.options['censys_query']
        c = CensysIPv4(api_id, api_secret)
        IPV4_FIELDS = [ 'ip', 
                        'protocols', 
                        'location.country', 
                        'location.latitude', 
                        'location.longitude',
                        '443.https.tls.certificate.parsed.names',
                        '25.smtp.starttls.tls.certificate.parsed.names', 
                        '110.pop3.starttls.tls.certificate.parsed.names',
                       ]
        try:
            payload = c.search(query, fields=IPV4_FIELDS)
        except CensysException as e:
            self.error('Error seen: {0}'.format(e))
            return
        for result in payload:
            names = set()
            for k,v in result.items():
                if k.endswith('.parsed.names'):
                    for name in v:
                        names.add(name)
            if len(names) < 1:
                # make sure we have at least a blank name
                names.add('')
            for name in names:
                if name.startswith('*.'):
                    self.add_domains(name.replace('*.', ''))
                    continue
                self.add_hosts(host=name,
                               ip_address=result['ip'], 
                               country=result.get('location.country', ''),
                               latitude=result.get('location.latitude', ''), 
                               longitude=result.get('location.longitude', ''))
                for protocol in result['protocols']:
                    port, service = protocol.split('/')
                    self.add_ports(ip_address=result['ip'], host=name, port=port, protocol=service)