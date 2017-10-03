#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from keehost_cli import list_entries

def dispatch(action="nop"):

    ''' Dispatch and do the action given in parameter '''

    actions = {
        'list': list_entries,
    }
    for a in actions:
        if a == action:
            return actions[a]()
    print("[+] Action not found !")

def main():

    ''' Main process '''
    parser = argparse.ArgumentParser(description="A command line tool to interact with a keehost api")
    parser.add_argument('--action', required=True, type=str, help="The action you want to do, allowed: list, create")
    args = parser.parse_args()
    return dispatch(args.action)

if __name__ == "__main__":
    main()
