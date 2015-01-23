#!/usr/bin/env python
import logging
from world import World

class AutoConnectException(Exception):
    pass

class PyKatObject(object):
    def __init__(self, name):
        self._pykat_object = None
        self.name = name
    
    def create_ports(self, ports, porttype):
        plist = []
        for pnames in ports:
            cp = porttype(self)
            plist.append(cp)
            if not (type(pnames) == tuple):
                pnames = (pnames,) # convert to tuple
            for pn in pnames:
                setattr(self, pn, cp)
        return plist

    def create_remaining_nodes(self):
        raise NotImplemented()

    @property
    def pykat_object(self):
        if self._pykat_object:
            return self._pykat_object
        else:
            logging.info('Creating pykat object for {0}'.format(self.name))
            self.create_remaining_nodes()
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

    def __setattr__(self, attr, value):
        # avoid infinite recursion with __getattr__ while _pykat_object is not set
        if attr != '_pykat_object' and self._pykat_object:
            if hasattr(self._pykat_object, attr):
                return self._pykat_object.__setattr__(attr,value)
        else:
            return super(PyKatObject,self).__setattr__(attr,value)

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