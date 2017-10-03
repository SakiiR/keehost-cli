# -*- coding: utf-8 -*-

from .models import Entry, Group

def list_entries():

    ''' Print all the entries owned by you on the console grouped by groups '''

    print("[^] Listing Groups and entries!\n")
    groups = {}
    for entry in Entry.list(params={'embedded': {'group': 1}}):
        if entry.group.name not in groups:
            groups[entry.group.name] = []
        groups[entry.group.name].append(entry)
    for group in groups:
        print("[^] %s:" % group)
        for entry in groups.get(group):
            # Display one entry
            print("[^]\t %s:%s" % (entry._id[20:], entry.name))
    print("[+] Done!")


