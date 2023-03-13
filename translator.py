import webserver
import socket
import _thread

def main():
    _thread.start_new_thread(webserver.run_server, ())

    transmitter = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("pong", 4242)

    pos = (7, 7)

    while True:
        old_pos = pos
        pos = webserver.get_pos()

        if not old_pos == pos:
            msg = str(pos[0]) + " " + str(pos[1])
            transmitter.sendto(msg.encode(), addr)


if __name__ == '__main__':
    main()