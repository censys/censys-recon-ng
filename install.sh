# variables
RECON_NG=~/.recon-ng
RECON_NG_MODULES=$RECON_NG/modules
RECON_NG_RECON_MODULES=$RECON_NG_MODULES/recon
RECON_NG_KEYS=$RECON_NG/keys.db

# installed check
if [ ! -d $RECON_NG ]; then
	echo "[-] Please install and run recon-ng before installing modules."
	exit 1
fi

# install context
echo "[*] Installing censys recon-ng modules..."
mkdir -p $RECON_NG_RECON_MODULES

# companies-contacts
mkdir -p $RECON_NG_RECON_MODULES/companies-contacts
cp recon/companies-contacts/censys_cert_emails.py $RECON_NG_RECON_MODULES/companies-contacts

# companies-domains
mkdir -p $RECON_NG_RECON_MODULES/companies-domains
cp recon/companies-domains/censys_cert_domains.py $RECON_NG_RECON_MODULES/companies-domains

# companies-multi
mkdir -p $RECON_NG_RECON_MODULES/companies-multi
cp recon/companies-multi/censys_asn_org.py $RECON_NG_RECON_MODULES/companies-multi
cp recon/companies-multi/censys_tls_org.py $RECON_NG_RECON_MODULES/companies-multi

# companies-netblocks
mkdir -p $RECON_NG_RECON_MODULES/companies-netblocks
cp recon/companies-netblocks/censys_asn_netname.py $RECON_NG_RECON_MODULES/companies-netblocks

# domains-companies
mkdir -p $RECON_NG_RECON_MODULES/domains-companies
cp recon/domains-companies/censys_domain_org.py $RECON_NG_RECON_MODULES/domains-companies

# domains-domains
mkdir -p $RECON_NG_RECON_MODULES/domains-domains
cp recon/domains-domains/censys_subdomains.py $RECON_NG_RECON_MODULES/domains-domains

# domains-hosts
mkdir -p $RECON_NG_RECON_MODULES/domains-hosts
cp recon/domains-hosts/censys_domain.py $RECON_NG_RECON_MODULES/domains-hosts

# hosts-hosts
mkdir -p $RECON_NG_RECON_MODULES/hosts-hosts
cp recon/hosts-hosts/censys_hostname.py $RECON_NG_RECON_MODULES/hosts-hosts
cp recon/hosts-hosts/censys_ip.py $RECON_NG_RECON_MODULES/hosts-hosts
cp recon/hosts-hosts/censys_query.py $RECON_NG_RECON_MODULES/hosts-hosts

# netblocks-companies
mkdir -p $RECON_NG_RECON_MODULES/netblocks-companies
cp recon/netblocks-companies/censys_netblock_company.py $RECON_NG_RECON_MODULES/netblocks-companies

# netblocks-hosts
mkdir -p $RECON_NG_RECON_MODULES/netblocks-hosts
cp recon/netblocks-hosts/censys_netblock.py $RECON_NG_RECON_MODULES/netblocks-hosts

# add keys
if [ -f "$RECON_NG_KEYS" ]; then
	echo "[*] Inserting censys recon-ng keys..."
	for key in censysio_id censysio_secret; do
		echo "INSERT OR IGNORE INTO keys (name) VALUES (\"$key\");" | sqlite3 $RECON_NG_KEYS
	done
else
	echo "[-] Please use the 'keys add' command to set 'censysio_id' and 'censysio_secret'."
fi

exit 0
