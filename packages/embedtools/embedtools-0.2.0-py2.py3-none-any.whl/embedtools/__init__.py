import random
import datetime
__version__ = "0.2.0"
__author__ = 'Lukas Canter'
__credits__ = 'Author'

# red = 0xFF1A1A
# orange = 0xFF751A
# yellow = 0xFFF81A
# lime = 0x4AFF1A
# green = 0x319718
# cyan = 0x23FFDA
# blue = 0x23B0FF
# purple = 0x2328FF
# magenta = 0xC523FF
# pink = 0xFF64CF
# black = 0x000000

class Colors:
    def rand():
        randomcolorchoice = random.randint(0, 0xffffff)
        return randomcolorchoice

    def choice(colorone, colortwo):
        randomcolorchoice = random.choice([colortwo, colorone])
        return randomcolorchoice
    
    def red():
        color = 0xFF1A1A
        return color
    def orange():
        color = 0xFF751A
        return color
    def yellow():
        color = 0xFFF81A
        return color
    def lime():
        color = 0x4AFF1A
        return color
    def green():
        color = 0x319718
        return color
    def cyan():
        color = 0x23FFDA
        return color
    def blue():
        color = 0x23B0FF
        return color
    def purple():
        color = 0x2328FF
        return color
    def magenta():
        color = 0xC523FF
        return color
    def pink():
        color = 0xFF64CF
        return color
    def black():
        color = 0x000000
        return color


class Timestamp:
    def time():
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        return timestamp

