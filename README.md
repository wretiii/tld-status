# tld-status
Enumeration tool for the registration status of an organization's domain against TLD's listed at https://data.iana.org/TLD/tlds-alpha-by-domain.txt.

Prerequisite:
```
pip install python-whois
```

Command syntax:
```
Usage: python script.py -d <domain_base>
Example: python script.py -d example
Options:
  -d  Specify the base domain to check against all TLDs from IANA list.
  -h, --help  Show this help message and exit.
```
