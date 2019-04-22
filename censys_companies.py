from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException

class Module(BaseModule):
    meta = {
        'name': 'Censys Companies by Domain',
        'author': 'J Nazario',
        'description': 'Retrieves the TLS certificates for a domain. Updates the \'companies\' table with the values from the subject organization information.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def module_run(self, domains):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret)
        IPV4_FIELDS = [ '443.https.tls.certificate.parsed.names',
                        '25.smtp.starttls.tls.certificate.parsed.names', 
                        '110.pop3.starttls.tls.certificate.parsed.names',
                        '443.https.tls.certificate.parsed.subject.organization',
                        '25.smtp.starttls.tls.certificate.parsed.subject.organization', 
                        '465.smtp.tls.tls.certificate.parsed.subject.organization', 
                        '587.smtp.starttls.tls.certificate.parsed.subject.organization',]
        for domain in domains:
            self.heading(domain, level=0)
            try:
                payload = [ x for x in c.search('mx:{0} OR 443.https.tls.certificate.parsed.names:{0} OR 25.smtp.starttls.tls.certificate.parsed.names:{0} OR 110.pop3.starttls.tls.certificate.parsed.names:{0}'.format(domain), IPV4_FIELDS) ]
            except CensysException:
                continue
            for result in payload:
                orgs = set()
                for k,v in result.items():
                    if k.endswith('.parsed.subject.organization'):
                        for org in v:
                            orgs.add(org)
                for org in orgs:
                    self.add_companies(company=org)