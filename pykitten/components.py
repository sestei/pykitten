#!/usr/bin/env python
import logging
from world import World
from pkobject import PyKatObject
from ports import Port, DumpPort

import pykat.components as pkc
from pykat.SIfloat import *

class Component(PyKatObject):
	def __init__(self, name, ports):
		super(Component,self).__init__(name)
		self._ports = self.create_ports(ports,Port)
		World.Instance().register_component(self)
	
class BeamDump(Component):
	def __init__(self):
		super(BeamDump, self).__init__('dump', [])
		self.input = DumpPort()
		self._ports = [self.input]

	def create_pykat_object(self):
		return None


class Space(Component):
	def __init__(self, name='', **kwargs):
		if not name:
			name = World.Instance().get_free_name('s')
		super(Space, self).__init__(name, [('a', 'input'),('b','output')])
		self._kwargs = kwargs

	def create_pykat_object(self):
		return pkc.space(
			self.name, 
			self.input.targetname,
			self.output.targetname,
			**self._kwargs
		)


def auto_reflectivity(kwargs):
	# if losses are given, we assume we already have a full mirror spec
	# and should not mess with it
	if 'L' in kwargs:
		return kwargs
	# otherwise, just assume R = 1-T
	if 'R' in kwargs and not 'T' in kwargs:
		kwargs['T'] = 1.0 - SIfloat(kwargs['R'])
	elif 'T' in kwargs and not 'R' in kwargs:
		kwargs['R'] = 1.0 - SIfloat(kwargs['T'])
	return kwargs

class Mirror(Component):
	def __init__(self, name, **kwargs):
		super(Mirror, self).__init__(name, [('a', 'west', 'input'),('b', 'east', 'output')])
		self._kwargs = auto_reflectivity(kwargs)

	def create_pykat_object(self):
		return pkc.mirror(
			self.name,
			self.west.targetname,
			self.east.targetname,
			**self._kwargs
		)

class BeamSplitter(Component):
	def __init__(self, name, **kwargs):
		super(BeamSplitter, self).__init__(name,
										  [('a', 'west'),
										   ('b', 'north'),
										   ('c', 'east'),
										   ('d', 'south')])
		self._kwargs = auto_reflectivity(kwargs)
		
	def create_pykat_object(self):
		return pkc.beamSplitter(
			self.name,
			self.west.targetname,
			self.north.targetname,
			self.east.targetname,
			self.south.targetname,
			**self._kwargs
		)

class Laser(Component):
	def __init__(self, name, **kwargs):
		super(Laser, self).__init__(name, [('a', 'output')])
		self._kwargs = kwargs

	def create_pykat_object(self):
		return pkc.laser(
			self.name, 
			self.output.targetname,
			**self._kwargs
		)

class Isolator(Component):
	"""
	TODO: optional output of dumped beam is not supported yet,
		  not sure how to implement this
	"""
	def __init__(self, name, **kwargs):
		super(Isolator, self).__init__(name, 
			[('a', 'input'), ('b', 'output')])
		self._kwargs = kwargs

	def create_pykat_object(self):
		return pkc.isolator(
				self.name,
				self.input.targetname,
				self.output.targetname,
				**self._kwargs
			)

class Lens(Component):
	def __init__(self, name, **kwargs):
		super(Lens, self).__init__(name, 
			[('a', 'input'), ('b', 'output')])
		self._kwargs = kwargs

	def create_pykat_object(self):
		return pkc.lens(
			self.name, 
			self.input.targetname,
			self.output.targetname,
			**self._kwargs
		)

class Squeezer(Component):
	def __init__(self, name, **kwargs):
		super(Squeezer, self).__init__(name, [('a', 'output')])
		self._kwargs = kwargs

	def create_pykat_object(self):
		return pkc.squeezer(
			self.name, 
			self.output.targetname,
			**self._kwargs
		)

class Modulator(Component):
	def __init__(self, name, f, midx, order, **kwargs):
		super(Modulator, self).__init__(name, 
			[('a', 'input'), ('b', 'output')])
		self._kwargs = kwargs
		self._f = f
		self._midx = midx
		self._order = order

	def create_pykat_object(self):
		return pkc.lens(
			self.name, 
			self.input.targetname,
			self.output.targetname,
			self._f,
			self._midx,
			self._order,
			**self._kwargs
		)