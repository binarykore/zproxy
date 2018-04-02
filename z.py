#! /usr/bin/env python
import socket, sys, threading
from thread import *


try:
	lp = int(raw_input("[*] Listener:"))
except KeyboardInterrupt:
	print("\n[*] Disturbed!")
	sys.exit()

def start(lp):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', lp))
		s.listen(5)
		print("[*] OK: 200")
	except Exception, e:
		print("[*] FAILED: 404")
		sys.exit(2)
	DATA = 1
	while(DATA):
		try:
			conn, addr = s.accept()
			data = conn.recv(4096)
			start_new_thread(conn_string, (conn,data,addr))
		except KeyboardInterrupt:
			s.close()
			print("[*] Signing Off!")
			sys.exit(1)
	s.close()
def conn_string(conn, data, addr):
	try:
		first_line = data.split("\n")[0]

		url = first_line.split(" ")[1]
		
		http_pos = url.find("://")
	
		if(http_pos == 4):
			print("[*] Running on Port 80.")
			port = 80
		elif(http_pos == -1):
			print("[*] Running on Port 443.")
			port = 443
		proxy_server(url, port, conn, addr, data)
	except Exception, e:
		pass
def proxy_server(webserver, port, x, addr, data):
	ws = webserver.split(":")[0]
	sp = webserver.split(":")[1]
	print("[*] Streaming Website: " + ws + ":" + sp)
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		try:
			wh = socket.gethostbyname(ws)
		except socket.gaierror:
			print("400: Error Host.")
			sys.exit()
			
		print("Host: 200 - " + wh)
		c.connect((wh, 80))
				
		try:
			c.send("GET / HTTP/1.1\r\n\r\n")
		except socket.error:
			print("Send Error!")
    			sys.exit()
		DATA = (1)
		while(DATA):
			if(len(c.recv(4096)) > 0):
				x.send(c.recv(4096))
				dar = float(len(c.recv(4096)))
				dar = float(dar / 4096)
				dar = "%.3s" % (str(dar))
				dar = "%s KB" % (dar)
				print("[*] Request Done: %s => %s <=" % (str(addr[0]),str(dar)))
				continue
			else:
				c.close()
				x.close()
	except socket.error, (value, message):
		c.close()
		x.close()
		sys.exit(1)
start(lp)
