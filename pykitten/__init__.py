#!/usr/bin/env python	
import logging
import world
import plotting
from components import *
from detectors import *

def get_world():
	return world.World.Instance()

def reset():
	global dump
	get_world().reset()
	dump = BeamDump()

def build():
    return get_world().build()

def show_kat_commands():
    get_world().show_kat_commands()

def xaxis(*args, **kwargs):
    get_world().xaxis(args, kwargs)

def plot(logscale='auto'):
    #TODO: maybe don't call run here, should be called explicitly by the user?
    return plotting.default_plot(get_world().run(), logscale)

def add_signal(target, amplitude, phase, name=None):
    get_world().add_signal(target, amplitude, phase, name)

#TODO: make better use of the logging possibilities, e.g. write to file
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.WARNING)

def set_log_level(level):
    l = logging.getLogger()
    l.level = level

# beam dump (providing 'dump' node) is always available
BeamDump()