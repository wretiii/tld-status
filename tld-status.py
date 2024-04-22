import requests
import whois
import sys
import logging
from concurrent.futures import ThreadPoolExecutor

# Suppress error messages from the whois library
logging.getLogger("whois.whois").setLevel(logging.CRITICAL)

def fetch_tlds():
    url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    response = requests.get(url)
    tlds = response.text.splitlines()
    return [tld.lower() for tld in tlds if not tld.startswith('#')]

def check_whois(domain):
    try:
        w = whois.whois(domain)
        if w.domain_name:
            return domain  # Return the domain if registered
    except whois.parser.PywhoisError:
        pass
    return None

def main(domain_base):
    tlds = fetch_tlds()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_whois, f"{domain_base}.{tld}") for tld in tlds]
        registered_domains = [future.result() for future in futures if future.result() is not None]
    return registered_domains

def print_help():
    print("Usage: python tld-status.py -d <domain_base>")
    print("Example: python tld-status.py -d example")
    print("Options:")
    print("  -d  Specify the base domain to check against all TLDs from IANA list.")
    print("  -h, --help  Show this help message and exit.")

if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()
    elif "-d" in sys.argv:
        domain_base = sys.argv[sys.argv.index("-d") + 1]
        registered_domains = main(domain_base)
        if registered_domains:
            print("The following domains are registered:")
            for domain in registered_domains:
                print(domain)
        else:
            print("No registered domains found.")
    else:
        print_help()
