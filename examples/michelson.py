### michelson.py
#
# Pykitten example of a simple Michelson interferometer,
# giving the quantum-noise limited sensitivity plot.
#
import sys

sys.path.append('..')

from pykitten import *

reset()
#set_log_level(0) # uncomment to show all messages

# create components
Laser('l1', P=1000)
Mirror('ETMX', R=1, mass=1)
Mirror('ETMY', R=1, mass=1, phi=45)
BeamSplitter('BS', R=0.5)
QNoiseD('sens', senstype='S', num_demods=1, f1=1)

# link everything together
l1 >> 1.0 >> BS.west
BS.north >> 1e3 >> ETMX
BS.east >> 1e3 >> ETMY
BS.south >> sens

# build pykat environment
build()

# add differential displacement signal to end mirrors
add_signal(ETMX.z, 0.5, 0)
add_signal(ETMY.z, 0.5, 180)

# tune signal frequency
xaxis('log', [1e-2, 1e3], signals.f, 400)

# use signal frequency for demodulation of detector
sens.f1.put(xaxis.x)

# set output y-axis to displacement
sens.scale = 'meter'

# print generated finesse commands
show_kat_commands()

# auto-generate a nice plot
plot()
	