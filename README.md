# tld-status
Enumeration tool for the registration status of an organization's domain against all TLD's.

Prerequisite:
```
pip install python-whois
```

Command syntax:
```
usage: tld-status.py [-h] [--tld-file TLD_FILE] [--output-file OUTPUT_FILE] [--output-format {txt,csv}] domain_name api_key

Domain Checker

positional arguments:
  domain_name           Domain name without the top-level domain (e.g., example)
  api_key               RapidAPI key

options:
  -h, --help            show this help message and exit
  --tld-file TLD_FILE   Path to custom TLD list file
  --output-file OUTPUT_FILE
                        Path to output file
  --output-format {txt,csv}
                        Output format (txt or csv)
```
