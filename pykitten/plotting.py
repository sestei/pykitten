#!/usr/bin/env python
import world
import pylab as pl

def decades(data):
    return pl.log10(abs(data.max() / data.min()))

def guess_logscale(data):
    if data.min() == 0.0:
        return False
    else:
        return 3 < decades(data) < 20

def pyplot_plot(data, logscale='auto'):
    #TODO: deal with 2nd yaxis
    #TODO: deal with 3d plots
    if logscale == 'auto':
        logx = guess_logscale(data.x)
        logy = guess_logscale(data.y)
    else:
        logx = 'x' in logscale
        logy = 'y' in logscale
    
    pl.plot(data.x, data.y)
    pl.grid(True)
    ax=pl.gca()
    if logx:
        ax.set_xscale('log')
    if logy:
        ax.set_yscale('log')
    pl.xlim((data.x[0], data.x[-1]))
    pl.xlabel(data.xlabel)
    pl.legend(data.ylabels)
    pl.title("pyKitten v{0} result\n".format(world.version())
             +str(data.runDateTime))
    pl.show()

def default_plot(results, logscale='auto'):
    return pyplot_plot(results, logscale)