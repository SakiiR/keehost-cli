#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from keehost_cli import (list_entries,
                         create_group,
                         delete_group,
                         create_entry,
                         get_entry,
                         delete_entry)

actions = {
    'list_all': list_entries,
    'create_group': create_group,
    'delete_group': delete_group,
    'create_entry': create_entry,
    'get_entry': get_entry,
    'delete_entry': delete_entry,
}

def dispatch(action="nop"):

    ''' Dispatch and do the action given in parameter '''

    for a in actions:
        if a == action:
            return actions[a]()
    print("[+] Action not found !")

def main():

    ''' Main process '''

    parser = argparse.ArgumentParser(description="A command line tool to interact with a keehost api")
    parser.add_argument('--action', required=True, type=str, help="The action you want to do, allowed: %s" % ', '.join(actions))
    args = parser.parse_args()
    status = dispatch(args.action)
    if not status:
        return print("[-] Failed !")
    print("[+] Success !")


if __name__ == "__main__":
    main()
