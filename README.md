pykitten
========  

PyKat made easy?

This is a very-early-stage development of a wrapper around [PyKat][1], which
itself is a wrapper around the interferometry simulation software [finesse][2].

The idea here is that while PyKat is a very powerful wrapper, it is too
cumbersome to quickly create small simulation setups with it. Commands to add
components are verbose and hide the structure of the setup that is to be
simulated. The underlying finesse syntax is more concise, and looks like this
for a simple Michelson interferometer:

```
  l l1 1.0 0.0 n1
  s s1 1.0 n1 n2
  bs bs1 0.5 0.5 0 0 n2 n3 n4 n5
  s s2 1.0 n3 n6
  m mYend 0.99 0.01 n6 n7
  s s3 1.0 n4 n8
  m mXend 0.99 0.01 n8 n9
  pd pd_dark n5

  xaxis mXend phi lin -90 90 100
  yaxis abs
```

Here's how the above looks like in pykitten (complete working example):

```python
  from pykitten import *
  
  Laser('l1', P=1)
  BeamSplitter('bs1', R=0.5)
  Mirror('mXend', R=0.9)
  Mirror('mYend', R=0.9)
  PD('pd_dark')

  l1 >> 1.0 >> bs1.west
  bs1.east >> 1.0 >> mXend
  bs1.north >> 1.0 >> mYend
  bs1.south >> pd_dark

  build()
  xaxis('lin', [-90,90], mXend.phi, 100)
  plot()
```

Notice the omission of node names where they are not needed, separation of
parameters and configuration, as well as the easy creation of spaces without
having to keep track of individual node names.

Goals of pykitten
-----------------
- provide an easy interface to quickly build simulations based on PyKat,
  in a text-editor environment
- few, simple commands for quick plotting etc.
- provide full access to PyKat if needed
- stick to the basics, more advanced simulations might still use pykitten
  for setting up the simulation, but will then use PyKat for all analysis

Status
------
- rudimentary work flow implemented
- very few components and commands supported
  
---
-- Sebastian Steinlechner, 2014

[1]: http://gwoptics.org/pykat
[2]: http://gwoptics.org/finesse
