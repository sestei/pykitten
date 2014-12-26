#!/usr/bin/env python   
import logging
import pykat
from utils import Singleton

PYKITTEN_VERSION = (0,0,1)

def version():
    return '.'.join(map(str,PYKITTEN_VERSION))

class AlreadyRegisteredException(Exception):
    pass

class NoKatException(Exception):
    def __init__(self):
        super(NoKatException,self).__init__(
            'No kat environment available, did you run build()?'
        )

@Singleton
class World(object):
    def __init__(self):
        self._components = []
        self._detectors = []
        self.nodes = NodeNetwork()

    # ==== WARNING WARNING WARNING ====
    # These two functions register/remove global variables in the main script.
    # This is completely un-pythonic, but makes our nice-and-simple 
    # syntax work automagically. Just be warned that there might be
    # dragons out there...
    def register(self, other):
        import __main__
        logging.info('Registering object "{0}"'.format(other.name))
        if hasattr(__main__, other.name):
            raise AlreadyRegisteredException(
                'An object called "{0}" already exists.'.format(other.name))
        setattr(__main__, other.name, other)

    def remove(self, other):
        import __main__
        logging.info('Removing object {0}'.format(other.name))
        try:
            delattr(__main__, other.name)
        except NameError:
            logging.warning('No object called "{0}" was registered.'.format(other.name))

    def get_free_name(self, shorthand):
        import __main__
        start_at = 1000
        while hasattr(__main__, shorthand + str(start_at)):
            start_at += 1
        logging.info('Auto-generated id: {0}'.format(shorthand + str(start_at)))
        return shorthand + str(start_at)

    def register_component(self, component):
        self.register(component)
        self._components.append(component)
    
    def register_detector(self, detector):
        self.register(detector)
        self._detectors.append(detector)

    def remove_component(self, component):
        self.remove(component)
        self._components.remove(component)

    def remove_detector(self, detector):
        self.remove(detector)
        self._detectors.remove(detector)

    def build(self):
        #TODO: do we indeed want to override any previous kat object?
        self._kat = pykat.finesse.kat()

        for c in self._components:
            # this is to handle the special case of the dump object, which
            # has no pykat representation
            pykat_object = c.pykat_object
            if pykat_object:
                self._kat.add(pykat_object)
        for d in self._detectors:
            self._kat.add(d.pykat_object)
        return self._kat

    def xaxis(self, args, kwargs):
        try:
            _xaxis = pykat.commands.xaxis(*args, **kwargs)
            self._kat.add(_xaxis)
        except AttributeError:
            raise NoKatException()


    def show_kat_commands(self):
        try:
            kat_commands = self._kat.generateKatScript()
            print ''.join(kat_commands)
        except AttributeError:
            raise NoKatException()

    def run(self):
        try:
            self._results = self._kat.run()
            return self._results
        except AttributeError:
            raise NoKatException()

    def reset(self):
        # not calling self.remove_component() etc. here because it would
        # modify the list and break the iteration
        for c in self._components:
            self.remove(c)
        for d in self._detectors:
            self.remove(d)
        self._components = []
        self._detectors = []
        self._kat = None
        self.nodes = NodeNetwork()

class NodeNetwork(object):
    def __init__(self):
        self._nodes = []
        self._node_counter = 1000

    def register(self, node):
        node.index = self.generate_unique_id()
        self._nodes.append(node)

    def remove(self, node):
        node.index = -1
        self._nodes.remove(node)

    def connect(self, node1, node2):
        self.remove(node2)
        node2.index = node1.get_index()

    def generate_unique_id(self):
        self._node_counter += 1
        return self._node_counter

    def __str__(self):
        l = []
        for node in self._nodes:
            l.append(node.name)
        return 'NodeNetwork('+str(l)+')'