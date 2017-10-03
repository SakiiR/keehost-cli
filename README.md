# keehost-cli

An example of keehost client in command line (Python).

## Usage

Coming soon

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
