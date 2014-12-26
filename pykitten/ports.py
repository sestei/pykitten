#!/usr/bin/python
import logging
from exceptions import *
from nodes import Node, DumpNode
import components

class Port(object):
	def __init__(self, targettype = Node, precedence=0):
		self.target = targettype()
		self.precedence = precedence
		self.reverse = False

	#HACKHACK: these are a bit ugly, but simplify automatic connection
	@property
	def input(self):
		return self

	@property
	def output(self):
		return self

	def connect(self, other):
		# auto-create space if only a distance or distance + refr. index is given
		if type(other) == int or type(other) == float:
			other = components.Space(L=other)
			logging.info('Auto-created space: %s', str(other))
		elif type(other) == tuple:
			other = components.Space(L=other[0], n=other[1])
			logging.info('Auto-created space: %s', str(other))

		op = other.input
		if op == self:
			logging.warning('Tried to connect port to itself.')
			return
		self.reverse = True
		if self.precedence >= op.precedence:
			logging.info('Connecting %s to %s => %s',
						 self.targetname, op.targetname, self.targetname)
			op.target.remove()
			op.target = self.target
		else:
			logging.info('Connecting %s to %s => %s',
						 self.targetname, op.targetname, op.targetname)
			self.target.remove()
			self.target = op.target
		return other

	@property
	def targetname(self):
		return self.target.name

	def __rshift__(self, other):
		return self.connect(other)

	def __str__(self):
		return "Port -> "+repr(self.targetname)


class DetectorPort(Port):
	def __init__(self):
		super(DetectorPort,self).__init__(precedence=-1000)

	@property
	def targetname(self):
		if self.reverse:
			return self.target.name + "*"
		else:
			return self.target.name

class DumpPort(Port):
	def __init__(self):
		super(DumpPort,self).__init__(targettype=DumpNode, precedence=1000)



