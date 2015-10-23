PyPaxos
==============

This is a python implementation of the [paxos algorithm](https://en.wikipedia.org/wiki/Paxos_(computer_science)). It requires python version 3.4+ to leverage [PEP 443](https://www.python.org/dev/peps/pep-0443/).

Installation
==============

You can install dependencies through pip.
```
$ pip3 install -r requirements.txt
```

You can install package using setup tools.
```
$ python setup.py install
```

Getting Started
==============

You can configure the paxos.json for a set of replicas. Below is an example config of a 3 replica cluster for replica "192.168.0.1".

```
{
    "address": "192.168.0.1",
    "address_of_replicas": ["192.168.0.1", "192.168.0.2", "192.168.0.3"],
}

```

An application running on each replica starts the paxos service by simply creating a Store instance.

```python
>>> from paxos.app.store import Store
>>> store = Store()

```

We can replicate data by assigning and updating values on the store object. Basic python types are supported (e.g. lists, sets, dicts, ints).

```python

>>> store.mylist = []
>>> store.mylist.append("Donald Duck")

```

We can access data by simply requesting the attribute previously assigned.

```python

>>> store.mylist[0]
"Donald Duck"

```

References
==============

- [The Part-Time Parliament](http://research.microsoft.com/en-us/um/people/lamport/pubs/lamport-paxos.pdf)
- [Paxos Made Simple](http://research.microsoft.com/en-us/um/people/lamport/pubs/paxos-simple.pdf)
