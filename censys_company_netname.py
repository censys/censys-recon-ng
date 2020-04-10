from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException

class Module(BaseModule):
    meta = {
        'name': 'Censys networks by organization name',
        'author': 'J Nazario',
        'version': 1.0,
        'description': 'Queries Censys by autonomous system name to find networks owned by the named company.  Updates the \'networks\' table with the results.',
        'required_keys': ['censysio_id', 'censysio_secret'],
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
    }

    def module_run(self, companies):
        """
        search by ASN name using censys, then dump CIDRs from bgpview
        """
        # XXX
        # we really like to know netnames so we alter the schema ...
        try:
            self.query('ALTER TABLE netblocks ADD COLUMN netname TEXT')
        except:
            # probably been here before
            pass
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret)
        IPV4_FIELDS = [ 'autonomous_system.description', 'autonomous_system.asn' ]
        seen = set()
        for company in companies:
            self.heading(company, level=0)
            try:
                query = 'autonomous_system.description: "{0}" OR autonomous_system.name: "{0}"'.format(company)
                payload = c.search(query, IPV4_FIELDS)
            except CensysException:
                continue
            for result in payload:
                asn = result.get('autonomous_system.asn', False)
                if not asn:
                    continue
                if asn in seen:
                    continue
                else:
                    seen.add(asn)
                    bgpview_url = 'https://api.bgpview.io/asn/{0}/prefixes'
                    routes = self.request('GET', bgpview_url.format(asn)).json()
                    for route in routes['data']['ipv4_prefixes']:                    
                        self.insert_netblocks(route['prefix'])
                        # XXX have to do this because we insert this data ourselves
                        self.query('UPDATE netblocks SET netname = "{0}" WHERE netblock = "{1}"'.format(result.get('autonomous_system.description', ''), route['prefix']))