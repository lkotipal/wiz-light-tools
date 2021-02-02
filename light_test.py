import time
import asyncio
from light import lights_random, lights_off, lights_normal, lights_red

while True:
    asyncio.run(lights_random())
    time.sleep(0.8)
    #asyncio.run(lights_off())
    #time.sleep(0.8)