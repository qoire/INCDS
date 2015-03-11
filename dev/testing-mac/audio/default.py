from pyo import *

s = Server().boot()
s.start()

wav = SquareTable()
env = CosTable([(0,0),(100,1),(500,.3),(8191,0)])
met = Metro(.125, 12).play()
amp = TrigEnv(met, table=env, dur=1, mul=.01)
pit = TrigXnoiseMidi(met, dist='loopseg', x1=20, scale=1, mrange=(48,84))
out = Osc(table=wav, freq=pit, mul=amp).out()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()
