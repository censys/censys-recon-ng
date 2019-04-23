from recon.core.module import BaseModule

from censys.ipv4 import CensysIPv4
from censys.base import CensysException

class Module(BaseModule):
    meta = {
        'name': 'Censys hosts by company',
        'author': 'J Nazario',
        'description': 'Harvests hosts from the Censys.IO API by using the \'autonomous_system.organization\' search operator. Updates the \'hosts\' and the \'ports\' tables with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
        'required_keys': ['censysio_id', 'censysio_secret'],        
    }

    def module_run(self, companies):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        c = CensysIPv4(api_id, api_secret)
        IPV4_FIELDS = [ 'ip', 'protocols', 'location.country', 
                        'location.latitude', 'location.longitude']                  
        for company in companies:
            self.heading(company, level=0)
            try:
                payload = [ x for x in c.search('autonomous_system.organization:"{0}"'.format(company), IPV4_FIELDS) ]
            except CensysException:
                continue
            for result in payload:
                self.add_hosts(ip_address=result['ip'], 
                               country=result.get('location.country', ''),
                               latitude=result.get('location.latitude', ''), 
                               longitude=result.get('location.longitude', ''))
                for protocol in result['protocols']:
                    port, service = protocol.split('/')
                    self.add_ports(ip_address=result['ip'], port=port, protocol=service)
