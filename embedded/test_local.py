import receiver
import _thread
import other

_thread.start_new_thread(other.runner, ())

receiver.run_server()