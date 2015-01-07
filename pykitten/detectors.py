#!/usr/bin/env python
from world import World
from ports import DetectorPort
from pkobject import PyKatObject

import pykat.detectors as pkd

class Detector(PyKatObject):
	def __init__(self, name, ports):
		super(Detector, self).__init__(name)
		self._ports = self.create_ports(ports, DetectorPort)
		World.Instance().register_detector(self)
	
	def __rshift__(self, other):
		# this is different to components, we always connect to the input
		return self.input >> other

class PD(Detector):
	def __init__(self, name, **kwargs):
		super(PD, self).__init__(name, ['input'])
		self._num_demods = 0
		if 'num_demods' in kwargs:
			self._num_demods = kwargs['num_demods']
			del(kwargs['num_demods'])
		self._kwargs = kwargs
		
	def create_pykat_object(self):
		# PYKAT BUG: in principle, pykat should autodetect n* node names,
		# but currently that behaviour seems to be overridden by the
		# alternate_beam class option. So we extract that information here again...
		alt = self.input.targetname[-1] == '*'
		return pkd.pd(
			self.name,
			self._num_demods 
			self.input.targetname,
			alternate_beam = alt,
			**self._kwargs
		)

class AD(Detector):
	def __init__(self, name, frequency, **kwargs):
		super(AD, self).__init__(name, ['input'])
		self._frequency = frequency
		self._kwargs = kwargs

	def create_pykat_object(self):
		alt = self.input.targetname[-1] == '*'
		return pkd.ad(
			self.name,
			self._frequency,
			self.input.targetname,
			alternate_beam = alt,
			**self._kwargs
		)

class BP(Detector):
	def __init__(self, name, direction, parameter):
		super(BP, self).__init__(name, ['input'])
		self._direction = direction
		self._parameter = parameter

	def create_pykat_object(self):
		alt = self.input.targetname[-1] == '*'
		return pkd.bp(
			self.name,
			self._direction,
			self._parameter,
			self.input.targetname,
			alternate_beam = alt
		)

class QnoiseD(Detector):
	def __init__(self, name, **kwargs):
		super(QnoiseD, self).__init__(name, ['input'])
		self._num_demods = 0
		if 'num_demods' in kwargs:
			self._num_demods = kwargs['num_demods']
			del(kwargs['num_demods'])
		self._kwargs = kwargs
		
	def create_pykat_object(self):
		alt = self.input.targetname[-1] == '*'
		return pkd.qnoised(
			self.name,
			self._num_demods 
			self.input.targetname,
			alternate_beam = alt,
			**self._kwargs
		)

class QShot(Detector):
	def __init__(self, name, **kwargs):
		super(QShot, self).__init__(name, ['input'])
		self._num_demods = 0
		if 'num_demods' in kwargs:
			self._num_demods = kwargs['num_demods']
			del(kwargs['num_demods'])
		self._kwargs = kwargs
		
	def create_pykat_object(self):
		alt = self.input.targetname[-1] == '*'
		return pkd.qshot(
			self.name,
			self._num_demods 
			self.input.targetname,
			alternate_beam = alt,
			**self._kwargs
		)

class Motion(Detector):
	def __init__(self, name, component, motion):
		super(QShot, self).__init__(name, [])
		self._component = component.name
		self._motion = motion
		
	def create_pykat_object(self):
		return pkd.qshot(
			self.name,
			None,
			self._component,
			self._motion
		)

class HD(Detector):
	def __init__(self, name, phase=180):
		super(HD, self).__init__(name, 
			[('a','input1'), ('b','input2')])
		self._phase = phase

	def create_pykat_object(self):
		return pkd.hd(
			self.name,
			self._phase,
			self.input1.targetname,
			self.input2.targetname,
		)

class QHD(Detector):
	def __init__(self, name, phase=180, **kwargs):
		super(QHD, self).__init__(name, 
			[('a','input1'), ('b','input2')])
		self._phase = phase
		self._kwargs = kwargs

	def create_pykat_object(self):
		return pkd.qhd(
			self.name,
			self._phase,
			self.input1.targetname,
			self.input2.targetname,
			**self._kwargs
		)
