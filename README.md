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

Components are connected with the `>>` operator,

```python
  l1 >> mXend
```

Numbers between components are automatically interpreted as spaces,

```python
  l1 >> 1.0 >> mXend
```
This creates a space of 1m between ``l1`` and ``mXend``. Optionally, you can specify a refractive index by giving a tuple, e.g. ``(1, 1.44)`` would create a 1m space with a refractive index of 1.44.

Node names can be omitted when there's an obvious input-output configuration, but can also be specified explicitly,

```python
  l1.output >> 1.0 >> mXend.fr
```
Here, ``fr`` is borrowed from Optickle, ``mXend.input`` can be used interchangeably (and ``mXend.output`` is the same as ``mXend.bk``). For components with more than two nodes, the node names cannot be ommitted.

For photo diodes, the connection direction makes a difference. This code will look at the light reflected from the mirror,
```python
  l1 >> 1.0 >> mXend
  pd >> mXend.input
```
(in this case, the ``.input`` could have been omitted). To look at the light coming from the laser, use:
```python
  l1 >> 1.0 >> mXend
  mXend.input >> pd
```
(here, the ``.input`` cannot be omitted, because ``mXend >> pd`` would normally expand to ``mXend.output >> pd.input`` and thus look at the transmitted light.)


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
