#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse

def login(url, username, password):

    ''' Login to the keehost REST Service 
   
        :param url A keehost login service URL
        :param username A keehost username
        :param password A keehost password

        :returns the allocated token or None
    '''

    r = requests.post(url.rstrip('/') + '/login', json={'username': username, 'password': password})
    data = r.json()
    return data.get('success'), data.get('message'), data.get('token')

def main():

    ''' Main process '''
    parser = argparse.ArgumentParser(description='Retrieve Keehost Token')
    parser.add_argument('--url', help="The keehost login service URL", type=str, required=True)
    parser.add_argument('--username', help="Your keehost username", type=str, required=True)
    parser.add_argument('--password', help="Your keehost password", type=str, required=True)
    args = parser.parse_args()
    success, message, token = login(url=args.url, username=args.username, password=args.password)
    print("[%s] %s %s" % (
        '+' if success else '-',
        message,
        token if success else ''
    ))

if __name__ == "__main__":
    main()




