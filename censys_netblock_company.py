from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException


class Module(BaseModule):
    meta = {
        'name': 'Censys organizations by netblock',
        'author': 'J Nazario',
        'version': '1.1',
        'description': 'Harvests organizations from the Censys API by searching netblocks. Updates the \'companies\' table with the results.',
        'query': 'SELECT DISTINCT netblock FROM netblocks WHERE netblock IS NOT NULL',
        'dependencies': ['censys'],
        'required_keys': ['censysio_id', 'censysio_secret'],
    }

    def module_run(self, netblocks):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret, timeout=self._global_options['timeout'])
        IPV4_FIELDS = [
            'autonomous_system.name',
        ]
        for netblock in netblocks:
            self.heading(netblock, level=0)
            try:
                # we only need one per netblock since they'll all have the same by ASN
                payload = c.search(
                    'ip:{0}'.format(netblock),
                    fields=IPV4_FIELDS,
                    max_records=2,
                )
            except CensysException:
                continue
            for result in payload:
                self.insert_companies(company=result['autonomous_system.name'])
