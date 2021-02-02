import time
import asyncio
from light import lights_random, lights_off, lights_normal, lights_red

asyncio.run(lights_red())