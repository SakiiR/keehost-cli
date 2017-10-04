# keehost-cli

An example of keehost client in command line (Python).

## Usage

Usage:

```sh
bash-3.2$ ./cli.py --help
usage: cli.py [-h] --action ACTION

A command line tool to interact with a keehost api

optional arguments:
  -h, --help       show this help message and exit
  --action ACTION  The action you want to do, allowed: list_all, create_group,
                   delete_group, create_entry, get_entry, delete_entry
```

Available actions are described in the help command.

### Creating group

A group is containing multiple entries.

```sh
bash-3.2$ ./cli.py --action create_group
[^] Group name: Social
[^] Creating group 'Social'
[+] Success !
```

### Creating entry

An entry is containing url, name, username and password.

```sh
bash-3.2$ ./cli.py --action create_entry
[^] Entry name: Facebook
[^] Group Name: Social
[^] Url: https://facebook.com
[^] Master password:
[^] Password to store: Password:
[^] Repeat password: Password:
[+] Success !
```

### Listing entries 

```sh
bash-3.2$ ./cli.py --action list_all
[^] Listing Groups and entries!

[G] Game
[E]      59d4a4563b6e3de4e5443c3e - Steam

[G] Social
[E]      59d4a41c3b6e3de4e5443c3c - Google
[E]      59d4a3cd3b6e3de4e5443c3b - Facebook

[+] Done!
[+] Success !
```

### Retrieving entry password

```sh
bash-3.2$ ./cli.py --action get_entry
[+] Entry ID: 59d4a41c3b6e3de4e5443c3c
[+] Master password:
[^] Here is your entry:
[^]      Name: Google
[^]      URL: https://facebook.com
[^]      Password: 456
[^]      Group: Social
[+] Success !
```

## Library

A REST client library is available. Example with groups:

```python
In [1]: from keehost_cli import *

In [2]: list(Group.list())
Out[2]: []

In [3]: g = Group()

In [4]: g.name = "toto"

In [5]: g.icon = None

In [6]: g.save()
Out[6]: True

In [7]: list(Group.list())
Out[7]: [<keehost_cli.models.group.Group at 0x10b9e8e80>]

In [8]: g = Group.find_one()

In [9]: Group.delete(identifier=g._id, etag=g._etag)
Out[9]: True

In [10]: list(Group.list())
Out[10]: []
```
