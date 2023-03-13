import socket
import select
import time

p1_pos = 7
p2_pos = 7

p1_conn = False
p2_conn = False


def get_pos():
    return p1_pos, p2_pos

def ready():
    return p1_conn and p2_conn


def launch_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    return server


def run_server():
    global p1_pos
    global p2_pos
    global p1_conn
    global p2_conn

    server = launch_server()

    with open("controller.html") as f:
        content = f.read()

    with open("player.html") as f:
        p_one = f.read()
        p_one = p_one.replace("SERVER_IP", "/p1")

    with open("player.html") as f:
        p_two = f.read()
        p_two = p_two.replace("SERVER_IP", "/p2")


    server.settimeout(0)
    server.listen(1)

    while True:
        try:
            client, addr = server.accept()
            #print(client, addr)

            r = None
            timeout = 20

            while not r:
                r, _, _ = select.select([client], [], [])
                time.sleep(0.001)
                timeout -= 1
                if timeout == 0:
                    client.close()
                    continue

            raw_request = client.recv(512).decode()
            request = str(raw_request)

            #print(raw_request)

            if "PUT" in request:
                player = request[6]
                value = request[7:9]

                if player == "1":
                    p1_pos = int(value)
                if player == "2":
                    p2_pos = int(value)

                #print("player", player)
                #print("value", value)

                response = 'HTTP/1.0 204 No Content\r\n\r\n'
                client.sendall(response.encode())
                #print("player one:", p1_pos)
                #print("player two:", p2_pos)

            elif "GET" in request:
                response = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
                client.sendall(response.encode())

                if "/p1" in request:
                    client.sendall(p_one.encode())
                    p1_conn = True

                elif "/p2" in request:
                    client.sendall(p_two.encode())
                    p2_conn = True

                elif "/reboot"in request:
                    client.sendall("<html><head>reboot</head> <body>rebooting now\n</body></html>")
                    client.close()
                    import machine
                    machine.reset()

                else:
                    client.sendall(content.encode())


            client.close()
        except OSError:
            pass
