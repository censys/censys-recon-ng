from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException


class Module(BaseModule):
    meta = {
        'name': 'Censys hosts by company',
        'author': 'J Nazario',
        'version': '1.1',
        'description': 'Harvests hosts from the Censys.IO API by using the \
            \'autonomous_system.organization\' search operator. \
                Updates the \'hosts\' and the \'ports\' tables with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
        'dependencies': ['censys'],
        'required_keys': ['censysio_id', 'censysio_secret'],
    }

    def module_run(self, companies):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret, timeout=self._global_options['timeout'])
        IPV4_FIELDS = [
            'ip',
            'protocols',
            '443.https.tls.certificate.parsed.names',
            '25.smtp.starttls.tls.certificate.parsed.names',
            '110.pop3.starttls.tls.certificate.parsed.names',
            'location.country',
            'location.latitude',
            'location.longitude',
            'location.province',
        ]
        for company in companies:
            self.heading(company, level=0)
            try:
                payload = c.search(
                    'autonomous_system.name:"{0}"'.format(company), IPV4_FIELDS
                )
            except CensysException:
                continue
            for result in payload:
                names_list = [
                    result.get('443.https.tls.certificate.parsed.names', []),
                    result.get('25.smtp.starttls.tls.certificate.parsed.names', []),
                    result.get(
                        '110.pop3.starttls.tls.certificate.parsed.names',
                        [],
                    ),
                ]
                names = set().union(*names_list)
                if len(names) < 1:
                    names.add('')
                for name in names:
                    if name.startswith('*.'):
                        self.insert_domains(domain=name.replace('*.', ''))
                        continue
                    self.insert_hosts(
                        ip_address=result['ip'],
                        host=name,
                        country=result.get('location.country', ''),
                        region=result.get('location.province', ''),
                        latitude=result.get('location.latitude', ''),
                        longitude=result.get('location.longitude', ''),
                    )

                for protocol in result['protocols']:
                    port, service = protocol.split('/')
                    self.insert_ports(
                        ip_address=result['ip'],
                        host=name,
                        port=port,
                        protocol=service,
                    )
