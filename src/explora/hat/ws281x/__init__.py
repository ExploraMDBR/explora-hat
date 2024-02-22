from .ws_2811_conf import ws, leds, channel
import colorsys
from collections.abc import Iterable
from math import ceil

def clamp(val, _min, _max):
    return max(min(val, _max), _min)

# new_index = max(0, min(new_index, len(mylist)-1))

class Color:
    def __init__(self, r=-1, g=-1, b=-1, h=-1, s=-1, v=-1):
        if r < 0 and g < 0 and b < 0:
            self.set_from_hsv(h,s,v)
        else:
            r = clamp(r,0,255)
            g = clamp(g,0,255)
            b = clamp(b,0,255)

            self._r = r/255
            self._g = g/255
            self._b = b/255
            
            self._h, self._s, self._v = colorsys.rgb_to_hsv(self._r, self._g, self._b)

#             self.value = r << 16 | g << 8 | b
            
    def set_from_hsv(self, h, s, v):
        if h < 0:
            h = 0
        h = h % 360

        s = clamp(s,0,100)
        v = clamp(v,0,100)
            
        self._h = h/360
        self._s = s/100
        self._v = v/100
        
        self._r, self._g, self._b = colorsys.hsv_to_rgb(self._h, self._s, self._v)
        
#         return int(round(self._r*255)) << 16 | int(round(self._g*255)) << 8 | int(round(self._b*255))
    
    @property
    def value(self):
        return int(round(self._r*255)) << 16 | int(round(self._g*255)) << 8 | int(round(self._b*255))
    
    @property
    def r(self):
        return round(self._r * 255)
    
    @r.setter
    def r(self,value):
        r = clamp(value,0,255)
        self._r = r/255
        
    @property
    def g(self):
        return round(self._g * 255)

    @g.setter
    def g(self,value):
        g = clamp(value,0,255)
        self._g = g/255
    
    @property
    def b(self):
        return round(self._b * 255)
    
    @b.setter
    def b(self,value):
        b = clamp(value,0,255)
        self._b = b/255
    
    @property
    def h(self):
        return round(self._h * 360)
    
    @h.setter
    def h(self,value):
        h = value % 360
        self._h = h / 360
        self._r, self._g, self._b = colorsys.hsv_to_rgb(self._h, self._s, self._v)
        
    @property
    def s(self):
        return round(self._s * 100)
    
    @s.setter
    def s(self,value):
        s = clamp(value,0,100)
        self._s = s/100
        self._r, self._g, self._b = colorsys.hsv_to_rgb(self._h, self._s, self._v)
        
    @property
    def v(self):
        return round(self._v * 100)
    
    @v.setter
    def v(self,value):
        v = clamp(value,0,100)
        self._v = v/100
        self._r, self._g, self._b = colorsys.hsv_to_rgb(self._h, self._s, self._v)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        self.n += 1
        if self.n == 1:
            return self.r
        elif self.n == 2:
            return self.g
        elif self.n == 3:
            return self.b
        else:
            raise StopIteration
    
    def copy(self):
        return Color(*tuple(self))

    def mix(self, other, weight = 0.5, inplace=False):
        w = clamp(weight,0,1)
        if isinstance(other, type(self)):
            o = tuple(other)
        elif isinstance(other, Iterable) and len(other) == 3:
            o = other
        else:
            raise ValueError("Color.mix() requires a Color or 3-value iterable object, received: {}".format(type(other)))

        new = [int(t * (1-w) + o[i] * w) for i,t in enumerate(tuple(self))  ]

        if inplace:
            self.r = new[0]
            self.g = new[1]
            self.b = new[2]
            return self
        
        return Color(*new)
        
    def __repr__(self):
        return "Color({:3d}, {:3d}, {:3d})".format(self.r, self.g, self.b)
        
    def __str__(self):
        return "Color r = {:3d}, g = {:3d}, b = {:3d} | h = {:3d}, s = {:3d}, v = {:3d}".format(self.r, self.g, self.b, self.h, self.s, self.v)


def set_leds(led_list):
    for i, l in enumerate(led_list):
        if type(l) is Color:
            l = l.value
        elif type(l) is int:
            pass
        else:
            raise TypeError("The led list must contain only `Color` or `int` types")

        ws.ws2811_led_set(channel, i, l)
        # print("Set led {}, color={}".format(i, l))

    resp = ws.ws2811_render(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

def bright_to_ascii(b):
	ascii_vals = ".,:+iwW#"
	return ascii_vals[int((len(ascii_vals) - 1) * b)];

def close():
    ws.ws2811_fini(leds)
    ws.delete_ws2811_t(leds)