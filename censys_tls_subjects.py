from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException

class Module(BaseModule):
    meta = {
        'name': 'Censys Companies by Domain',
        'author': 'J Nazario',
        'description': 'Retrieves the TLS certificates for a domain.  Updates the \'ports\' table with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
        'required_keys': ['censysio_id', 'censysio_secret'],        
    }

    def module_run(self, companies):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret)
        IPV4_FIELDS = [ 'ip', 
                        'protocols', 
                        'location.country', 
                        'location.latitude', 
                        'location.longitude',
                        '443.https.tls.certificate.parsed.names',
                        '25.smtp.starttls.tls.certificate.parsed.names', 
                        '110.pop3.starttls.tls.certificate.parsed.names',
                        '443.https.tls.certificate.parsed.subject.organization',
                        '25.smtp.starttls.tls.certificate.parsed.subject.organization', 
                        '465.smtp.tls.tls.certificate.parsed.subject.organization', 
                        '587.smtp.starttls.tls.certificate.parsed.subject.organization',]
        for company in companies:
            self.heading(company, level=0)
            try:
                payload = c.search('443.https.tls.certificate.parsed.subject.organization:"{0}" OR 25.smtp.starttls.tls.certificate.parsed.subject.organization:"{0}" OR 465.smtp.tls.tls.certificate.parsed.subject.organization:"{0}" OR 587.smtp.starttls.tls.certificate.parsed.subject.organization:"{0}"'.format(company), IPV4_FIELDS)
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