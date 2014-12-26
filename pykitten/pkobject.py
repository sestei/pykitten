#!/usr/bin/env python
import logging
from world import World

class AutoConnectException(Exception):
    pass

class PyKatObject(object):
    def __init__(self, name):
        self.name = name
        self._pykat_object = None
    
    def create_ports(self, ports, porttype):
        plist = []
        for pnames in ports:
            cp = porttype()
            plist.append(cp)
            if not (type(pnames) == tuple):
                pnames = (pnames,) # convert to tuple
            for pn in pnames:
                setattr(self, pn, cp)
        return plist

    @property
    def pykat_object(self):
        if self._pykat_object:
            return self._pykat_object
        else:
            logging.info('Creating pykat object for {0}'.format(self.name))
            self._pykat_object = self.create_pykat_object()
            return self._pykat_object
    
    def create_pykat_object(self):
        raise NotImplemented()

    def __getattr__(self, attr):
        if self._pykat_object:
            return getattr(self._pykat_object, attr)
        else:
            return AttributeError(("'{0}' has no attribute '{1}'. " +
                    "Did you try to access pykat properties before calling build()?").format(
                        self.__class__.__name__, attr))

    @property
    def input(self):
        try:
            return self._input
        except AttributeError:
            raise AutoConnectException('no default input node available')

    @input.setter
    def input(self, value):
        self._input = value

    @property
    def output(self):
        try:
            return self._output
        except AttributeError:
            raise AutoConnectException('no default output node available')

    @output.setter
    def output(self, value):
        self._output = value

    def __rshift__(self, other):
        return self.output >> other

    def __str__(self):
        s = self.__class__.__name__ + " " + self.name + ': ('
        targets = [p.targetname for p in self._ports]
        s += ' '.join(targets)
        return s+')'