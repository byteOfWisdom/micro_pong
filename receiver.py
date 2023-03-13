import socket

p1_pos = 7
p2_pos = 7


def get_pos():
	return p1_pos, p2_pos

def ready():
	return p1_pos != 7 and p2_pos != 7


def launch_server():
    addr = socket.getaddrinfo('0.0.0.0', 4242)[0][-1]
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(addr)
    return server


def run_server():
	global p1_pos
	global p2_pos

	server = launch_server()

	while True:
		data, _ = server.recvfrom(5)
		player_data = data.decode().split()
		p1_pos = int(player_data[0])
		p2_pos = int(player_data[1])
		print(p1_pos, p2_pos)