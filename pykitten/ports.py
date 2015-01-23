#!/usr/bin/python
import logging
from exceptions import *
from nodes import Node, DumpNode
import components

class AlreadyLinked(Exception):
	def __init__(self, port):
		super(AlreadyLinked, self).__init__(
			str(port.parent)
		)
		

class Port(object):
	def __init__(self, parent, targettype = Node, precedence=0):
		self.targettype = targettype
		self.target = None
		self.parent = parent
		self.precedence = precedence

	def set_target(self, target):
		if self.target:
			raise AlreadyLinked(self)
		self.target = target

	def is_detector(self):
		return False

	#HACKHACK: these are a bit ugly, but simplify automatic connection
	@property
	def input(self):
		return self

	@property
	def output(self):
		return self

	@staticmethod
	def connect(lhs, rhs):
		# auto-create space if only a distance or distance + refr. index is given
		if type(rhs) == int or type(rhs) == float:
			rhs = components.Space(L=rhs)
			logging.info('Auto-created space: %s', str(rhs))
		elif type(rhs) == tuple:
			rhs = components.Space(L=rhs[0], n=rhs[1])
			logging.info('Auto-created space: %s', str(rhs))

		rhs_p = rhs.input
		if rhs_p == lhs:
			logging.warning('Tried to connect port to itself')
			return
		
		if lhs.precedence > rhs_p.precedence:
			lhs.create_target()
			lhs.target.add(rhs_p)
		else:
			rhs_p.create_target()
			rhs_p.target.add(lhs)

		return rhs 

	def create_target(self):
		if not self.target:
			self.target = self.targettype(self)
		return self.target

	@property
	def targetname(self):
		if self.target:
			return self.target.name
		else:
			return 'UNCONNECTED'

	def __rshift__(self, other):
		return self.connect(self, other)

	def __str__(self):
		return "Port -> "+repr(self.targetname)


class DetectorPort(Port):
	def __init__(self, parent):
		super(DetectorPort,self).__init__(parent, precedence=-1000)
		self.reverse = False

	def is_detector(self):
		return True

	def __rshift__(self, other):
		self.connect(self, other)
		self.reverse = True
		return other

	@property
	def targetname(self):
		if not self.target:
			return 'UNCONNECTED'
		elif self.reverse:
			return self.target.name + "*"
		else:
			return self.target.name

class DumpPort(Port):
	def __init__(self, parent):
		super(DumpPort,self).__init__(parent, targettype=DumpNode,precedence=1000)
		self.create_target()

	def set_target(self, target):
		logging.warning('DumpPort.set_target called, this should not happen as it should always take precedence.')




