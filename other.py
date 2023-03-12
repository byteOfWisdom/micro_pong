from time import sleep
import webserver

def runner():
	while True:
		sleep(1)
		print(webserver.get_pos())