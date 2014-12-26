#!/usr/bin/env python
from world import World

class Node(object):
	def __init__(self):
		self.index = -1;
		World.Instance().nodes.register(self)

	@property
	def name(self):
		if self.index < 0:
			return 'INVALID'
		return 'n' + str(self.index)

	def remove(self):
		try:
			World.Instance().nodes.remove(self)
		except ValueError:
			pass

	def __str__(self):
		return "Node('"+self.name+"')"

class DumpNode(Node):
	def __init__(self):
		super(DumpNode, self).__init__()

	@property
	def name(self):
		return 'dump'

	def remove(self):
		log.debug('tried to remove DumpNode')
		return

