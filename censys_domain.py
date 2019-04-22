from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException

class Module(BaseModule):
    meta = {
        'name': 'Censys Hosts and Subdomains by Domain',
        'author': 'J Nazario',
        'description': 'Retrieves the MX records, SMTPS, POP3S, and HTTPS for a domain. Updates the \'hosts\' and the \'ports\' tables with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def module_run(self, domains):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret)
        IPV4_FIELDS = [ 'ip', 'protocols', 'location.country', 
                        'location.latitude', 'location.longitude',
                        '443.https.tls.certificate.parsed.names',
                        '25.smtp.starttls.tls.certificate.parsed.names', 
                        '110.pop3.starttls.tls.certificate.parsed.names']          
        for domain in domains:
            self.heading(domain, level=0)
            try:
                payload = [ x for x in c.search('mx:{0} OR 443.https.tls.certificate.parsed.names:{0} OR 25.smtp.starttls.tls.certificate.parsed.names:{0} OR 110.pop3.starttls.tls.certificate.parsed.names:{0}'.format(domain), IPV4_FIELDS) ]
            except CensysException:
                continue
            for result in payload:
                names = set()
                for k,v in result.items():
                    if k.endswith('.parsed.names'):
                        for name in v:
                            names.add(name)
                if len(names) > 0:
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
                