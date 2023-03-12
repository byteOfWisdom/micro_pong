import webserver
import _thread
import other

_thread.start_new_thread(other.runner, ())

webserver.run_server()