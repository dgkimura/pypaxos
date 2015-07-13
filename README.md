PyPaxos
==============

This is a python implementation of the [paxos algorithm](https://en.wikipedia.org/wiki/Paxos_(computer_science)). It requires python version 3.4+.

Installation
==============

You can install dependencies through pip.
```
$ pip install -r requirements.txt
```

You can install package using setup tools.
```
$ python setup.py install
```

Algorithm
==============

Phases
- 1a: Prepare: Proposer creates proposal N
- 1b: Promise: Acceptor sends promise for proposal N. Promise includes
      previous proposal/value V.
- 2a: Accept Request
- 2b: Accepted

Phase 1 is unnecessary after the first round with stable leader and when
including instance number I in Promise, Accept, and Accepted.


```
Client   Proposer      Acceptor     Learner
   |         |          |  |  |       |  | --- First Request ---
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Prepare(N)
   |         |<---------X--X--X       |  |  Promise(N,I,{Va,Vb,Vc})
   |         X--------->|->|->|       |  |  Accept!(N,I,Vm)
   |         |<---------X--X--X------>|->|  Accepted(N,I,Vm)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |  --- Following Requests ---
   X-------->|          |  |  |       |  |  Request
   |         X--------->|->|->|       |  |  Accept!(N,I+1,W)
   |         |<---------X--X--X------>|->|  Accepted(N,I+1,W)
   |<---------------------------------X--X  Response
   |         |          |  |  |       |  |

```

References
==============

[Wikipedia Paxos](https://en.wikipedia.org/wiki/Paxos_(computer_science))
[Paxos Made Simple](http://research.microsoft.com/en-us/um/people/lamport/pubs/paxos-simple.pdf)
