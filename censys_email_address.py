from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException


class Module(BaseModule):
    meta = {
        'name': 'Censys hosts by domain',
        'author': 'J Nazario',
        'version': '1.1',
        'description': 'Retrieves the email address from the TLS certificates for a company. Updates the \'contacts\' table with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
        'dependencies': ['censys'],
        'required_keys': ['censysio_id', 'censysio_secret'],
    }

    def module_run(self, companies):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret, timeout=self._global_options['timeout'])
        IPV4_FIELDS = [
            '443.https.tls.certificate.parsed.issuer.email_address',
            '25.smtp.starttls.tls.certificate.parsed.issuer.email_address',
            '465.smtp.tls.tls.certificate.parsed.issuer.email_address',
            '587.smtp.starttls.tls.certificate.parsed.issuer.email_address',
            '1521.oracle.banner.tls.certificate.parsed.issuer.email_address',
            '3306.mysql.banner.tls.certificate.parsed.issuer.email_address',
            '3389.rdp.banner.tls.certificate.parsed.issuer.email_address',
            '5432.postgres.banner.tls.certificate.parsed.issuer.email_address',
            '8883.mqtt.banner.tls.certificate.parsed.issuer.email_address',
        ]
        SEARCH_FIELDS = [
            '443.https.tls.certificate.parsed.subject.organization',
            '25.smtp.starttls.tls.certificate.parsed.subject.organization',
            '465.smtp.tls.tls.certificate.parsed.subject.organization',
            '587.smtp.starttls.tls.certificate.parsed.subject.organization',
            '1521.oracle.banner.tls.certificate.parsed.subject.organization',
            '3306.mysql.banner.tls.certificate.parsed.subject.organization',
            '3389.rdp.banner.tls.certificate.parsed.subject.organization',
            '5432.postgres.banner.tls.certificate.parsed.subject.organization',
            '8883.mqtt.banner.tls.certificate.parsed.subject.organization',
        ]
        for company in companies:
            self.heading(company, level=0)
            try:
                query = ' OR '.join(
                    ['{0}:"{1}"'.format(x, company) for x in SEARCH_FIELDS]
                )
                payload = c.search(query, IPV4_FIELDS)
            except CensysException as e:
                self.error('Exception: {0}'.format(e))
                continue
            for result in payload:
                for k, v in result.items():
                    if k.endswith('.issuer.email_address'):
                        for email in v:
                            self.insert_contacts(email=email)
