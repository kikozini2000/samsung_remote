#!/usr/bin/env python3.5

import time
import socket
import argparse
import sys
import csv
import ssdp
import re
import samsungctl
import urllib.request
import xml.etree.ElementTree as ET

def namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''

def getTVinfo(url):
    ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', url)
    xmlinfo = urllib.request.urlopen(url)
    xmlstr = xmlinfo.read().decode('utf-8')
    root = ET.fromstring(xmlstr)
    ns = namespace(root)
    fn = root.find('.//{}friendlyName'.format(ns)).text
    model = root.find('.//{}modelName'.format(ns)).text
    return {'fn': fn, 'ip': ip.group(0), 'model': model}

def push(ip, key, wait_time = 100.0):
    try:
        config = {
            "name": "samsungctl",
            "description": "PC",
            "id": "",
            "host": ip,
            "port": 55000,
            "method": "legacy",
            "timeout": 0,
        }

        with samsungctl.Remote(config) as remote:
            remote.control(key)

        time.sleep(wait_time / 1000.0)
        return True

    except socket.error:
        return False

def scan_network_ssdp(verbose):
    try:
        tv_list = []
        if (verbose):
            print("Scanning network...")
        tvs_found = ssdp.discover("urn:samsung.com:device:RemoteControlReceiver:1", timeout=1);
        for tv in tvs_found:
            info = getTVinfo(tv.location)
            tv_list.append(info)
            if (verbose):
                print(info['fn'] + " found in ip: " + info['ip'])
        return tv_list

    except KeyboardInterrupt:
        print (' was pressed. Search interrupted by user')

def execute_macro(ip, filename):
    try:
      with open(filename, newline='') as macro_file:
          config = {
              "name": "samsungctl",
              "description": "PC",
              "id": "",
              "host": ip,
              "port": 55000,
              "method": "legacy",
              "timeout": 0,
          }
          reader = csv.DictReader(macro_file, ("key", "time"))

          with samsungctl.Remote(config) as remote:
              for line in reader:
                  key = line['key']
                  if (key.startswith('#')):
                      continue
                  remote.control(key)
                  time.sleep(float(line['time'] or 1000.0) / 1000.0)

    except (FileNotFoundError, IOError):
        print('No such macro file: ' + filename) 

def main():
    parser = argparse.ArgumentParser(description='Controls your Samsumg SmartTV thru Wifi')
    parser.add_argument("-s", "--scan", help="scans the TV on the network", action="store_true")
    parser.add_argument("-k", "--key", help="the key to be sent to TV")
    parser.add_argument("-p", "--poweroff", help="search all TV's in the network and turn them off", action="store_true")
    parser.add_argument("-i", "--ip", help="defines the ip of the TV that will receive the command")
    parser.add_argument("-a", "--auto", help="sends the command to the first TV available", action="store_true")
    parser.add_argument("-m", "--macro", help="the macro file with commands to be sent to TV")

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    dst = ''

    if args.scan:
        scan_network_ssdp(True)

    if args.auto:
        tvs = scan_network_ssdp(False)
        if tvs is not None:
            dst = tvs[0]

    if args.ip:
        dst = args.ip

    if args.key:
        push(dst, args.key)

    if args.poweroff:
        tvs = scan_network_ssdp(False)
        if tvs is not None:
            for tv in tvs:
                print("Turning off " + tv['fn'] + " ... ", end='')
                if push(tv['ip'], 'KEY_POWEROFF'):
                    print('success.')
                else:
                    print('failed.')

    if args.macro:
        execute_macro(dst, args.macro)

if __name__ == "__main__": main()
