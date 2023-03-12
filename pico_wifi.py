import network
import socket
import time

from machine import Pin

from credentials import ssid, password


def launch_wifi():
    led = Pin("LED", Pin.OUT)

    network.hostname("pong")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)


    max_wait = 5
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep_ms(2)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
        return None
    else:
        led.value(1)
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        return status[0]