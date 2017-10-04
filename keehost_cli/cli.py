# -*- coding: utf-8 -*-

import sys
import getpass
from .models import Entry, Group
from .crypto import AESCipher

def read_string(prompt="[^] Input: "):

    ''' Read a string from stdin
   
        :params prompt The string to display before reading (without \n)
    '''

    print("%s" % prompt, end='', flush=True)
    inp = sys.stdin.readline().splitlines()
    if len(inp) == 0:
        return ''
    return inp[0]


def list_entries():

    ''' Print all the entries owned by you on the console grouped by groups '''

    print("[^] Listing Groups and entries!\n")
    groups = {}
    for entry in Entry.list(params={'embedded': {'group': 1}}):
        if entry.group:
            if entry.group.name not in groups:
                groups[entry.group.name] = []
            groups[entry.group.name].append(entry)
    for group in Group.list():
        if group.name not in groups:
            groups[group.name] = []
    for group in groups:
        print("├── %s" % group)
        if len(groups.get(group)) == 0:
            print("[^] Empty !")
        for entry in groups.get(group):
            print("├    ├── %s - %s" % (entry._id, entry.name))
    print("\n[+] Done!")
    return True

def create_group():

    ''' It creates a group in the API '''

    name = read_string(prompt="[^] Group name: ")
    print("[^] Creating group '%s'" % name)
    group = Group()
    group.icon = None
    group.name = name
    return group.save()

def _find_group():

    found = False
    while not found:
        group = Group.find_one(params={'where': {'name': read_string('[^] Group Name: ')}})
        if group is not None:
            found = True
        else:
            print("Group not found ! try again !")
    return group

def _find_entry():
    found = False
    while not found:
        entry = Entry.find_one(params={
            'where': {
                '_id': read_string('[+] Entry ID: ')
            }, 
            'embedded': {
                'group': 1
            }
        })
        if entry is not None:
            found = True
        else:
            print("Entry not found ! try again !")
    return entry

def _read_password(prompt="[^] Password: "):

    ''' Read password from stdin '''

    
    print("%s" % prompt, end='', flush=True)
    return getpass.getpass()


def _read_passwords():

    ''' Read the two passwords from stdin '''

    ok = False
    while not ok:
        value1 = _read_password(prompt="[^] Password to store: ")
        value2 = _read_password(prompt="[^] Repeat password: ")
        if value1 == value2 and len(value1) > 0:
            ok = True
        else:
            print("[-] Passwords incorrects, try again")
    return value1


def create_entry():

    ''' It creates an entry in the API '''

    entry = Entry()
    entry.icon = None
    entry.name = read_string("[^] Entry name: ")
    entry.username = read_string("[^] Username: ")
    entry.group = _find_group()._id
    entry.url = read_string("[^] Url: ")
    aes = AESCipher(key=_read_password(prompt="[^] Master password: "))
    entry.value = aes.encrypt(_read_passwords())
    return entry.save()


def delete_group():

    ''' It deletes a group from the eve api '''

    name = read_string(prompt='[+] Group name: ')
    group = Group.find_one(params={'where': {'name': name}})
    status = False
    if group is not None:
        status = Group.delete(identifier=group._id, etag=group._etag)
        if not status:
            print("[-] Failed to delete group %s:'%s'" % (group._id, group.name))
    else:
        print("[-] Group by name '%s' was not found" % name)
    return status


def delete_entry():

    ''' Delete a stored entry '''

    entry = _find_entry()
    print("[^] Deleting entry '%s'" % entry.name)
    return Entry.delete(identifier=entry._id, etag=entry._etag)


def get_entry():

    ''' Retrieve entry password '''

    entry = _find_entry()
    aes = AESCipher(key=_read_password(prompt="[+] Master password"))
    password = aes.decrypt(entry.value)
    print("[^] Here is your entry: ")
    print("[^]\t Name: %s" % entry.name)
    print("[^]\t URL: %s" % entry.url)
    print("[^]\t Username: %s" % entry.username)
    print("[^]\t Password: %s" % password)
    if entry.group is not None:
        print("[^]\t Group: %s" % entry.group.name)
    return True
