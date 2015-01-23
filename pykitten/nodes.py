#!/usr/bin/env python
from world import World

class TooManyConnections(Exception):
	pass

class DetectorConnectedToDumpNode(Exception):
	pass

class Node(object):
	def __init__(self, parent):
		self.index = -1;
		self.parents = [parent]
		self.detectors = []
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

	def add(self, parent):
		parent.set_target(self)
		if parent.is_detector():
			self.detectors.append(parent)
		else:
			if len(self.parents) < 2:
				self.parents.append(parent)
			else:
				raise TooManyConnections(self)

	def __str__(self):
		return "Node('"+self.name+"')"

class DumpNode(Node):
	#def __init__(self, parent):
	#	super(DumpNode, self).__init__(parent)

	@property
	def name(self):
		return 'dump'

	def add(self, parent):
		if parent.is_detector():
			raise DetectorConnectedToDumpNode(parent)

		parent.set_target(self)
		# for a dump node, we don't care how many ports are connected
		self.parents.append(parent)

	def remove(self):
		log.debug('tried to remove DumpNode')
		return

