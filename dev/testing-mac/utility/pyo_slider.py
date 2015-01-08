from pyo import *
import time

s = Server().boot()
s.start()
ifs = [350,360,375,388]
maps = [SLMap(20., 2000., 'log', 'freq', ifs), SLMap(0, 0.25, 'lin', 'feedback', 0), SLMapMul(.1)]
a = SineLoop(freq=ifs, mul=.1).out()
#a.ctrl(maps)

time.sleep(10)
