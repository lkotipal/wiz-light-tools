import datetime
import time
import asyncio
from light import lights_normal

tmin = datetime.time(8)
tmax = datetime.time(9)
while True:
    t = datetime.datetime.now().time()
    if t > tmin and t < tmax:
        asyncio.run(lights_normal())
        print("On!")
        while True:
            t = datetime.datetime.now().time()
            if t > tmax:
                print("Waiting!")
                break
    time.sleep(600)