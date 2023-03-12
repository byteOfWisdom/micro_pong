import array, time
from machine import Pin
import rp2



# Configure the number of WS2812 LEDs.
NUM_LEDS = 256
DIMX = 16
DIMY = 16
FREQ = 800_000
TIMESTEP = 5

R_SHIFT = 16
G_SHIFT = 24
B_SHIFT = 8

# 0xff = 8bits all 1
R_MASK = 0xff << R_SHIFT
G_MASK = 0xff << G_SHIFT
B_MASK = 0xff << B_SHIFT


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    wrap_target()

    label("bitloop")
    out(x, 1)               .side(0)    [1 - 1]

    jmp(not_x, "do_zero")   .side(1)    [1 - 1]
    jmp("bitloop")          .side(1)    [4 - 1]

    label("do_zero")
    nop()                   .side(0)    [4 - 1]

    wrap()


def launch_sm():
    sm_frequency = TIMESTEP * FREQ

    # Create the StateMachine with the ws2812 program, outputting on Pin(22).
    # maybe freq is wrong
    sm = rp2.StateMachine(0, ws2812, freq = sm_frequency, sideset_base=Pin(2))

    # Start the StateMachine, it will wait for data on its FIFO.
    sm.active(1)
    return sm



def rgb_to_value(r, g, b):
    return (r << R_SHIFT) | (g << G_SHIFT) | (b << B_SHIFT)


def value_to_rgb(value):
    r = (R_MASK & value) >> R_SHIFT
    g = (G_MASK & value) >> G_SHIFT
    b = (B_MASK & value) >> B_SHIFT
    return (r, g, b)


led_buffer = array.array("I", [0 for _ in range(NUM_LEDS)])
sm = launch_sm()


def set_led_num(n):
    NUM_LEDS = n
    led_buffer = array.array("I", [0 for _ in range(NUM_LEDS)])


def set_xy(x, y, r, g, b):
    if x >= DIMX or y >= DIMY: return
    if x < 0 or y < 0: return
    index = ((y * 16) + (16 - x) - 1)

    if y % 2:
        index = (y * 16) + x

    led_buffer[index] = rgb_to_value(r, g, b)


def set_xy_value(x, y, value):
    if x >= DIMX or y >= DIMY: return
    if x < 0 or y < 0: return
    index = ((y * 16) + (16 - x) - 1)

    if y % 2:
        index = (y * 16) + x

    led_buffer[index] = value


def get_xy(x, y):
    if x >= DIMX or y >= DIMY: return 0
    if x < 0 or y < 0: return 0

    index = ((y * 16) + (16 - x) - 1)

    if y % 2:
        index = (y * 16) + x

    return led_buffer[index]


def set(index, r, g, b):
    led_buffer[index] = rgb_to_value(r, g, b)


def reset():
	for i in range(NUM_LEDS):
		led_buffer[i] = 0


#push the current array state to the leds
def push(wait = 50):
    sm.put(led_buffer, NUM_LEDS)
    time.sleep_ms(wait)