import asyncio
import numpy as np
from pywizlight.bulb import wizlight, PilotBuilder
import colorsys

# CW from leftmost light
lights = (wizlight("192.168.0.122"), wizlight("192.168.0.162"), wizlight("192.168.0.154"))
rng = np.random.default_rng()

# Todo: randomize hue to be different than previous
async def light_random(light):
    # uniform random ints
    # pb = PilotBuilder(rgb = tuple(map(lambda i: int(i), rng.integers(0, 256, size=3))))
    # Dirichlet distribution
    #rgbs = np.round(255*np.random.dirichlet([1, 1, 1], 2))
    # HSV with maximum saturation and value
    state = await lights[light].updateState()
    oldrgb = tuple(map(lambda i: i/255, state.get_rgb()))
    oldhue = int(255 * colorsys.rgb_to_hsv(oldrgb[0], oldrgb[1], oldrgb[2])[0])
    while True:
        hue = rng.uniform(0, 360, 1)
        print(oldhue)
        print(hue)
        if abs(hue - oldhue) > 100 or (360 - oldhue + hue > 100) or (360 - hue + oldhue > 100):
            break
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    await lights[light].turn_on(PilotBuilder(rgb = tuple(map(lambda i: int(255*i), rgb))))

async def lights_random():
    # create/get the current thread's asyncio loop
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        light_random(0),
        light_random(1),
        light_random(2),
        loop = loop
    )

async def lights_red():
    # create/get the current thread's asyncio loop
    loop = asyncio.get_event_loop()
    rgb = [1, 0, 0]
    pb = PilotBuilder(rgb = rgb)
    await asyncio.gather(
        lights[0].turn_on(pb),
        lights[1].turn_on(pb),
        lights[2].turn_on(pb),
        loop = loop
    )

async def lights_off():
    # create/get the current thread's asyncio loop
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        lights[0].turn_off(),
        lights[1].turn_off(),
        lights[2].turn_off(),
        loop = loop
    )

async def lights_normal():
    loop = asyncio.get_event_loop()
    pb = PilotBuilder()
    await asyncio.gather(
        lights[0].turn_on(pb),
        lights[1].turn_on(pb),
        lights[2].turn_on(pb),
        loop = loop
    )