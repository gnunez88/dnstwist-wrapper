#!/usr/bin/env python3

import argparse
import json
import signal
import sys


def stop(sig, frame):
    sys.stderr.write('\n[!] Exiting...\n')
    sys.exit(1)


def main(args):
    signal.signal(signal.SIGINT, stop)

    #fields = ['domain', 'fuzzer', 'dns_a', 'dns_aaaa', 'dns_ns', 'dns_mx', 'banner_http']

    with open(args.json_file, 'r') as f:
        contents = json.load(f)

    header  = "Domain"
    header += " Fuzzer"
    header += " Banner"
    header += " IPv4"
    header += " IPv6" if args.all else ""
    header += " MX" if args.all else ""
    header += " NS" if args.all else ""
    print(header)

    separator  = f"{'-'*len('Domain')}"
    separator += f" {'-'*len('Fuzzer')}"
    separator += f" {'-'*len('Banner')}"
    separator += f" {'-'*len('IPv4')}"
    separator += f" {'-'*len('IPv6')}" if args.all else ""
    separator += f" {'-'*len('MX')}" if args.all else ""
    separator += f" {'-'*len('NS')}" if args.all else ""
    print(separator)

    for entry in contents:
        register  = f"{entry['domain']}"
        register += f" {entry['fuzzer']}"
        register += f" {entry['banner_http'] if 'banner_http' in entry else '-'}"
        register += f" {','.join(entry['dns_a']) if 'dns_a' in entry else '-'}"
        register += f" {','.join(entry['dns_aaaa']) if len('dns_aaaa') in entry else '-'}" if args.all else ""
        register += f" {entry['dns_mx'] if len('dns_mx') in entry else '-'}" if args.all else ""
        register += f" {entry['dns_ns'] if len('dns_ns') in entry else '-'}" if args.all else ""
        print(register)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', type=str, help="JSON file (dnstwist output)")
    parser.add_argument('-o', '--outfile', type=str, help="Output file")
    parser.add_argument(
            '-a', '--all', 
            action='store_true', 
            default=False, 
            help="Show all the fields")
    args = parser.parse_args()
    main(args)
