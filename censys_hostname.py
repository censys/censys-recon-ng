from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException


class Module(BaseModule):
    meta = {
        'name': 'Censys hosts by hostname',
        'author': 'J Nazario',
        'version': '1.1',
        'description': 'Finds all IPs for a given hostname. Updates the "hosts" and "ports" tables.',
        'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL',
        'dependencies': ['censys'],
        'required_keys': ['censysio_id', 'censysio_secret'],
    }

    def module_run(self, hosts):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret, timeout=self._global_options['timeout'])
        IPV4_FIELDS = [
            'ip',
            'protocols',
            'location.country',
            'location.latitude',
            'location.longitude',
            'location.province',
        ]
        for host in hosts:
            self.heading(host, level=0)
            try:
                payload = c.search('a:{0}'.format(host), IPV4_FIELDS)
            except CensysException:
                continue
            for result in payload:
                self.insert_hosts(
                    host=host,
                    ip_address=result['ip'],
                    country=result.get('location.country', ''),
                    region=result.get('location.province', ''),
                    latitude=result.get('location.latitude', ''),
                    longitude=result.get('location.longitude', ''),
                )
                for protocol in result['protocols']:
                    port, service = protocol.split('/')
                    self.insert_ports(
                        ip_address=result['ip'], port=port, protocol=service
                    )
