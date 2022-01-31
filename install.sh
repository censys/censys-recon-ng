#!/usr/bin/env bash

RECON_DIR=~/.recon-ng/modules/recon

mkdir -p $RECON_DIR/companies-contacts
cp censys_email_address.py $RECON_DIR/companies-contacts

mkdir -p $RECON_DIR/companies-domains
cp censys_subdomains.py $RECON_DIR/companies-domains

mkdir -p $RECON_DIR/companies-multi
cp censys_org.py $RECON_DIR/companies-multi
cp censys_tls_subjects.py $RECON_DIR/companies-multi

mkdir -p $RECON_DIR/contacts-domains
cp censys_email_to_domains.py $RECON_DIR/contacts-domains

mkdir -p $RECON_DIR/domains-companies
cp censys_companies.py $RECON_DIR/domains-companies

mkdir -p $RECON_DIR/domains-hosts
cp censys_domain.py $RECON_DIR/domains-hosts

mkdir -p $RECON_DIR/hosts-hosts
cp censys_query.py $RECON_DIR/hosts-hosts

mkdir -p $RECON_DIR/hosts-ports
cp censys_hostname.py $RECON_DIR/hosts-ports
cp censys_ip.py $RECON_DIR/hosts-ports

mkdir -p $RECON_DIR/netblocks-companies
cp censys_netblock_company.py $RECON_DIR/netblocks-companies

mkdir -p $RECON_DIR/netblocks-hosts
cp censys_netblock.py $RECON_DIR/netblocks-hosts

for key in censysio_id censysio_secret; do
	echo "INSERT or IGNORE INTO keys (name) VALUES (\"$key\");" | sqlite3 ~/.recon-ng/keys.db
done

echo "Successfully installed Censys recon-ng modules."
exit 0