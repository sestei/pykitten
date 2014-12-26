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
		self._kwargs = kwargs

	def create_pykat_object(self):
		# PYKAT BUG: in principle, pykat should autodetect n* node names,
		# but currently that behaviour seems to be overridden by the
		# alternate_beam class option. So we extract that information here again...
		alt = self.input.targetname[-1] == '*'
		return pkd.pd(
			self.name,
			0, #TODO: num_demods 
			self.input.targetname,
			alternate_beam = alt,
			**self._kwargs
		)
