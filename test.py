import _thread
import webserver
import pong
import pico_wifi


ip = pico_wifi.launch_wifi()

_thread.start_new_thread(pong.run_game, ())

webserver.run_server()