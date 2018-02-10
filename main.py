import argparse
import math
import phue
import random
import rgb_cie
import sys
import time
import noise

FAILURE_COOLDOWN = 10  # ms

MOOD_COLOR = (0xc9, 0x8c, 0x60)

RAVE_COLORS = [
    [2, 216, 27],
    [15, 86, 193],
    [193, 15, 164],
    [255, 187, 0],
    [255, 0, 0],
    [0, 229, 255],
    [255, 0, 242]
]

random.seed()
converter = rgb_cie.Converter()


class Animator(object):
    def __init__(self, bridge, layout, resolution):
        self.b = bridge
        self.layout = layout
        self.layoutIds = [l['id'] for l in self.layout]
        self.resolution = resolution
        self.failures = 0

    def set_light(self, *args, **kwargs):
        try:
            self.b.set_light(*args, **kwargs)
            self.failures = 0
        except Exception:
            if self.failures == 2:
                print 'retry failed; re-throwing exception'
                raise
            self.b.connect()
            self.failures += 1
            time.sleep(FAILURE_COOLDOWN / 1000)
            self.set_light(*args, **kwargs)

    def on(self):
        self.set_light(self.layoutIds, 'on', True)

    def off(self):
        self.set_light(self.layoutIds, 'on', False)

    def on_now(self):
        self.set_light(self.layoutIds, 'on', True, transitiontime=0)

    def off_now(self):
        self.set_light(self.layoutIds, 'on', False, transitiontime=0)

    def strobe_randomly(self, glitter=False, rave=False):
        self.on_now()
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(255, 255, 255), transitiontime=0)
        self.off_now()
        # reduce the amount of commands that are issued
        ons = set()
        offs = set()
        slids = set(self.layoutIds)
        while True:
            on_lights = set(random.sample(self.layoutIds, random.randint(1, math.ceil(len(self.layoutIds) / 2))))
            self.set_light(on_lights - ons, 'on', True, transitiontime=0)
            if rave:
                self.set_light(on_lights - ons, 'xy', converter.rgbToCIE1931(*RAVE_COLORS[random.randint(0, len(RAVE_COLORS) - 1)]), transitiontime=0)
            self.set_light(on_lights - ons, 'bri', 254, transitiontime=0)
            self.set_light((slids - on_lights - offs), 'on', False, transitiontime=0)
            if glitter:
                self.set_light(on_lights - ons, 'on', False, transitiontime=0)
            ons = on_lights
            offs = set(slids - on_lights)
            time.sleep(0.1)

    def glitter(self):
        self.strobe_randomly(True)

    def glitter_rave(self):
        self.strobe_randomly(True, True)

    def strobe(self):
        self.on_now()
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(255, 255, 255), transitiontime=0)
        self.off_now()
        while True:
            self.set_light(self.layoutIds, 'on', True, transitiontime=0)
            self.set_light(self.layoutIds, 'bri', 254, transitiontime=0)
            time.sleep(0.1)
            self.set_light(self.layoutIds, 'on', False, transitiontime=0)
            time.sleep(0.1)

    def white(self):
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(255, 255, 255))

    def moody_fast(self):
        self.moody(increment=1.5)

    def moody(self, increment=0.5):
        self.fullbright()
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(*MOOD_COLOR), transitiontime=3)

        ticker = 0

        while True:
            ticker += increment
            for lid in self.layoutIds:
                valx = lid + math.sin(lid) * 10 + ticker
                val = noise.pnoise2(valx, ticker) * 254
                self.set_light(lid, 'bri', int(val), transitiontime=60)
                time.sleep(0.8)

    def relax(self):
        self.on_now()
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(*MOOD_COLOR))
        self.fullbright()

    def sex(self):
        self.on_now()
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(*MOOD_COLOR))
        self.set_light(self.layoutIds, 'bri', 80)

    def nite(self):
        self.on_now()
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(*MOOD_COLOR))
        self.set_light(self.layoutIds, 'bri', 1, transitiontime=60)

    def fullbright(self):
        self.on()
        self.set_light(self.layoutIds, 'bri', 254)

    def fullbright_now(self):
        self.on()
        self.set_light(self.layoutIds, 'bri', 254, transitiontime=0)

    def punch(self):
        self.fullbright_now()
        self.set_light(self.layoutIds, 'on', False, transitiontime=3)

    def punch_long(self):
        self.fullbright_now()
        self.set_light(self.layoutIds, 'on', False, transitiontime=30)

    def rainbow(self, factor=1):
        self.on()
        self.fullbright()
        unit3 = (math.pi * 2) / 3
        unit = (math.pi * 2) / (len(self.layoutIds) * factor)
        t = 0
        while True:
            offset = 0
            for lid in self.layoutIds:
                x = t + offset
                r = max(math.sin(x), 0)
                g = max(math.sin(x + unit3), 0)
                b = max(math.sin(x + (2 * unit3)), 0)
                xy = converter.rgbToCIE1931(r * 255, g * 255, b * 255)
                self.set_light(lid, 'xy', xy, transitiontime=((10 * factor) * self.resolution))
                offset += unit
            t += self.resolution
            time.sleep(self.resolution)

    def rainbow_weighted(self):
        self.rainbow(2)

    def rainbow_weighted3(self):
        self.rainbow(3)

    def rainbow_weighted4(self):
        self.rainbow(4)

    def rave(self, bpm=128):
        self.fullbright_now()

        while True:
            for lid in self.layoutIds:
                self.set_light(lid, 'xy', converter.rgbToCIE1931(*RAVE_COLORS[random.randint(0, len(RAVE_COLORS) - 1)]), transitiontime=0)
                self.set_light(lid, 'bri', 254, transitiontime=0)
            time.sleep(60 / bpm)

    def rave_fast(self):
        self.rave(bpm=400)

    def blue(self):
        self.set_light(self.layoutIds, 'on', True)
        self.set_light(self.layoutIds, 'bri', 254)
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(0, 0, 255))

    def red(self):
        self.set_light(self.layoutIds, 'on', True)
        self.set_light(self.layoutIds, 'bri', 254)
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(255, 0, 0))

    def purple(self):
        self.set_light(self.layoutIds, 'on', True)
        self.set_light(self.layoutIds, 'bri', 254)
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(200, 0, 255))

    def green(self):
        self.set_light(self.layoutIds, 'on', True)
        self.set_light(self.layoutIds, 'bri', 254)
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(0, 255, 50))

    def orange(self):
        self.set_light(self.layoutIds, 'on', True)
        self.set_light(self.layoutIds, 'bri', 254)
        self.set_light(self.layoutIds, 'xy', converter.rgbToCIE1931(255, 120, 0))

    def shard(self):
        colors = [
            [178, 91, 117],
            [255, 243, 86],
            [255, 61, 119],
            [28, 40, 204],
            [80, 50, 178]
        ]
        index = 0
        for lid in self.layoutIds:
            self.set_light(lid, 'on', True)
            self.set_light(lid, 'xy', converter.rgbToCIE1931(*colors[index]))
            index = (index + 1) % len(colors)

    def tv(self):
        self.on()
        for i in range(0, 3):
            self.set_light(self.layoutIds[i], 'bri', 200)
        for i in range(3, 5):
            self.set_light(self.layoutIds[i], 'bri', 80)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fun Philips Hue stuff')
    parser.add_argument('--list', action='store_true', help='List all lights and their IDs')
    parser.add_argument('--layout', help='A comma delimited list of lights to sequence, in order (defualts to whatever Hue gives us)')
    parser.add_argument('--resolution', type=float, default=0.6, help='The amount of time between frames. High resolutions (lower amounts) may crash your connection (shouldn\'t hurt anything though).')
    parser.add_argument('bridge_ip', help='The Hue Bridge IP address')
    parser.add_argument('anim', help='The animation to play')
    args = parser.parse_args()

    print 'initializing bridge'
    b = phue.Bridge(args.bridge_ip)
    print 'connecting'
    b.connect()
    print 'retrieving state'
    state = b.get_api()

    lights = state['lights']
    for k, v in lights.iteritems():
        v['id'] = int(k)

    if args.list:
        for light in lights.values():
            print '{}: {}'.format(light['id'], light['name'])
        sys.exit(2)

    layout = None
    if not args.layout:
        layout = lights.values()
    else:
        layout = [lights[a] for a in args.layout.split(',')]

    print 'initializing animator'
    ani = Animator(b, layout, args.resolution)
    print 'beginning animation'
    getattr(ani, args.anim)()
