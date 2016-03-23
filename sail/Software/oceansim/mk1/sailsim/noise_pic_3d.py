#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import math
from PIL import Image

perm = range(256)
random.seed(1)
random.shuffle(perm)
perm += perm
dirs = [(math.cos(a * 2.0 * math.pi / 256),
         math.cos((a+85) * 2.0 * math.pi / 256),
         math.cos((a+170) * 2.0 * math.pi / 256))
         for a in range(256)]

def noise(x, y, z, per):
    def surflet(gridX, gridY, gridZ):
        distX, distY, distZ = abs(x-gridX), abs(y-gridY), abs(z-gridZ)
        polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
        polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
        polyZ = 1 - 6*distZ**5 + 15*distZ**4 - 10*distZ**3
        hashed = perm[perm[perm[int(gridX)%per] + int(gridY)%per] + int(gridZ)%per]
        grad = (x-gridX)*dirs[hashed][0] + (y-gridY)*dirs[hashed][1] + (z-gridZ)*dirs[hashed][2]
        return polyX * polyY * polyZ * grad
        
    intX, intY, intZ = int(x), int(y), int(z)
    return (surflet(intX+0, intY+0, intZ+0) + surflet(intX+0, intY+0, intZ+1) + surflet(intX+0, intY+1, intZ+0) +
            surflet(intX+0, intY+1, intZ+1) + surflet(intX+1, intY+0, intZ+0) + surflet(intX+1, intY+0, intZ+1) +
            surflet(intX+1, intY+1, intZ+0) + surflet(intX+1, intY+1, intZ+1))
            
def fBm(x, y, z, per, octs):
    val = 0
    for o in range(octs):
        val += 0.5**o * noise(x*2**o, y*2**o, z*2**o, per*2**o)
    return val
    
size, freq, octs = 128, 1/32.0, 5

rCurve = [0, 2, 4, 150, 12, 16, 20, 30, 40, 50, 60, 70, 90, 120, 180, 250, 255]
gCurve = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 170, 200, 220, 245, 250, 250, 255]
bCurve = [10, 20, 30, 40, 50, 60, 70, 80, 90, 110, 130, 190, 200, 253, 254, 255, 255]
aCurve = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 170, 200, 220, 245, 250, 250, 255]

for z in range (size):
	data = []  
	print z  
	for y in range(size):
		for x in range(size):
			fBmVal = fBm(x*freq, y*freq, z*freq, int(size*freq), octs)
			iV = int(fBmVal*16) % 16
			
			data.append((int(rCurve[iV] + (rCurve[iV+1] - rCurve[iV]) * (fBmVal - iV/16)), 
					int(gCurve[iV] + (gCurve[iV+1] - gCurve[iV]) * (fBmVal - iV/16)),
					int(bCurve[iV] + (bCurve[iV+1] - bCurve[iV]) * (fBmVal - iV/16)),
					int(aCurve[iV] + (aCurve[iV+1] - aCurve[iV]) * (fBmVal - iV/16))))
        
	im = Image.new("RGBA", (size, size))
	im.putdata(data, 128.0, 128.0)
	im.save("test"+format(z, '03d')+".png")

print "finished doing it"

