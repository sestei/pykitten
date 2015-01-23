### cavity.py
#
# Simple pykitten example showing a cavity scan,
# with photo detectors in transmission and reflection
#
import sys

sys.path.append('..')

from pykitten import *

reset()
#set_log_level(0) # uncomment to show all messages

# create components
Laser('l1', P=1)
Mirror('ITM', R=0.9)
Mirror('ETM', R=0.9)
PD('pd_trans')
PD('pd_refl')

# link components together
l1 >> 1.0 >> ITM >> 1.0 >> ETM >> pd_trans
ITM.input >> pd_refl

# create pykat environment
build()

# scan phase of cavity end mirror
xaxis('lin', [-45, 45], ETM.phi, 400)

# show generated finesse script
show_kat_commands()

# make a plot of the output
plot()
	