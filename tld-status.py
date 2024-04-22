import argparse
import requests
import time
import csv
import itertools
import sys

def download_tlds(url):
    # Request TLDs from the given URL and filter out comments (lines starting with '#')
    response = requests.get(url)
    if response.status_code == 200:
        tlds = [line.strip() for line in response.text.split('\n') if not line.startswith('#')]
        return tlds
    else:
        raise Exception(f"Failed to download TLD list from {url}")

def generate_full_domains(domain_name, tlds):
    # Generate full domain names by appending TLDs to the base domain name
    return [f"{domain_name}.{tld}" for tld in tlds]

def check_domains(api_key, domains):
    # Check domain availability using the Domainr API and return results
    url = "https://domainr.p.rapidapi.com/v2/status?mashape-key=" + api_key + "&domain="
    headers = {
        "X-RapidAPI-Host": "domainr.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }
    results = []
    for domain in domains:
        response = requests.get(url + domain, headers=headers)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'N/A')
            results.append((domain, status))
    return results

def spinner():
    # Simple spinner for visual feedback during long operations
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while True:
        sys.stdout.write(next(spinner))   # write the next character
        sys.stdout.flush()                # flush stdout buffer (actual character display)
        sys.stdout.write('\b')            # erase the last written char
        time.sleep(0.2)

def save_results(results, output_file, format):
    # Save domain check results to a file in specified format (TXT or CSV)
    if format == 'txt':
        with open(output_file, 'w') as file:
            for domain, status in results:
                file.write(f"Domain: {domain}\nStatus: {status}\n\n")
        print(f"Results saved to {output_file}")
    elif format == 'csv':
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Domain', 'Status'])
            writer.writerows(results)
        print(f"Results saved to {output_file}")

def main():
    # Parse command line arguments and perform domain checks
    parser = argparse.ArgumentParser(description='Domain Checker')
    parser.add_argument('domain_name', help='Domain name without the top-level domain (e.g., example)')
    parser.add_argument('api_key', help='RapidAPI key')
    parser.add_argument('--output-file', default=None, help='Path to output file')
    parser.add_argument('--output-format', choices=['txt', 'csv'], default='txt', help='Output format (txt or csv)')
    
    args = parser.parse_args()
    domain_name = args.domain_name.lower()
    api_key = args.api_key
    output_file = args.output_file
    output_format = args.output_format

    tlds = download_tlds('https://data.iana.org/TLD/tlds-alpha-by-domain.txt')
    full_domains = generate_full_domains(domain_name, tlds)

    print("Enumerating all TLDs from https://data.iana.org/TLD/tlds-alpha-by-domain.txt.")
    print("This will take some time. Feel free to grab a drink and relax or move on to other OSINT tasks.")

    # Start spinner in a separate thread
    import threading
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    results = check_domains(api_key, full_domains)

    # Stop the spinner
    spinner_thread.do_run = False
    spinner_thread.join()

    for domain, status in results:
        print(f"Domain: {domain}\nStatus: {status}\n")

    if output_file is not None:
        save_results(results, output_file, output_format)

if __name__ == '__main__':
    main()
