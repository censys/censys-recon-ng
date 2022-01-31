# Censys `recon-ng` Modules

[![License](https://img.shields.io/github/license/censys/censys-recon-ng)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)
[![Code Style](https://img.shields.io/badge/code%20style-pycodestyle-blue)](https://github.com/PyCQA/pycodestyle)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

We have written several modules for [`recon-ng`](https://github.com/lanmaster53/recon-ng) adding data via the Censys API. These were inspired by the work that [@scumsec](https://github.com/scumsec/Recon-ng-modules) did on the original recon-ng additions from their add-on modules, and also from the subdomain enumeration techniques that use Censys data like from [@christophetd](https://github.com/christophetd/censys-subdomain-finder).

## Installation

We have provided two pieces you need to install these modules and begin using them.

- `requirements.txt` - Use this via `pip install -r requirements.txt` to install Python dependencies.
- `install.sh`- Run this script and it will both install the modules in your home directory (recon-ng supports modules added for the local user in `~/.recon-ng`) and configures the database to add support for your Censys API ID and secret. See your Censys [account](https://search.censys.io/account/api) for your credentials, and add them to the database as you would any other credential - `keys add ...`.

One you have completed these you can fire up `recon-ng`.

Configure your Censys API ID and secret variables using `keys add` to `censysio_id` and `censysio_secret`.

## Usage

These are normal recon-ng modules, use them like any other. Pivot away! This repository adds the following new modules:

```recon-ng
[recon-ng][default] > modules search censys
[*] Searching for 'censys'...

  Recon
  -----
    recon/companies-contacts/censys_email_address
    recon/companies-domains/censys_subdomains
    recon/companies-multi/censys_org
    recon/companies-multi/censys_tls_subjects
    recon/contacts-domains/censys_email_to_domains
    recon/domains-companies/censys_companies
    recon/domains-hosts/censys_domain
    recon/hosts-hosts/censys_query
    recon/hosts-ports/censys_hostname
    recon/hosts-ports/censys_ip
    recon/netblocks-companies/censys_netblock_company
    recon/netblocks-hosts/censys_netblock
```
