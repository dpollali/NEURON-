from neuron import n, gui
from neuron.units import *
import matplotlib.pyplot as plt
from bokeh.io import output_notebook
import bokeh.plotting as plt

output_notebook()

""" 
TUTORIAL 
"""

class BallandStick:
    def __init__(self,gid):
        self.__gid = gid
        self._setup_morphology()
        self._setup_biophysics()

    def _setup_morphology(self):
        self.soma = n.Section('Soma', self)
        self.dend = n.Section('Dendrite', self)
        self.dend.connect(self.soma)
        self.all = self.soma.wholetree()
        self.soma.L = self.soma.diam = 12.6157 * mm
        self.dend.L = 200 * mm
        self.dend.diam = 1 * mm

    def _setup_biophysics(self): #units S/cm^2
        for sec in self.all:
            sec.Ra = 100
            sec.cm = 1
        self.soma.insert(n.hh)
        for seg in self.soma:
            seg.hh.gnabar = 0.12
            seg.hh.gkbar = 0.036
            seg.hh.gl = 0.0003
            seg.hh.el = -54.3 * mV

        self.dend.insert(n.pas)

        for seg in self.dend:
            seg.pas.g = 0.001
            seg.pas.e = -65 * mV

    def __repr__(self):
        return "BallandStick[{}]".format(self.__gid)

my_cell = BallandStick(0)
area = f'{my_cell.soma(0.5).area():.2f}'

print(area)
n.topology()
print(n.units('gnabar_hh'))
for sec in n.allsec():
    print("%s: %s" % (sec, ", ".join(sec.psection()["density_mechs"].keys())))

"""
Stimulation of the neuronal cell
"""

stim = n.IClamp(my_cell.dend(1))
stim.delay = 5
stim.dur = 1
stim.amp = 0.1
soma_v = n.Vector().record(my_cell.soma(0.5)._ref_v)
t = n.Vector().record(n._ref_t)
n.finitialize(-65 * mV)
n.continuerun(25 * ms)




