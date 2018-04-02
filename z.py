#! /usr/bin/env python
import socket, sys, threading, re
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
	dta = 1
	while(dta):
		try:
			f, a = s.accept()
			start_new_thread(conn_string, (f, f.recv(4096), a))
		except KeyboardInterrupt:
			s.close()
			print("[*] Signing Off!")
			sys.exit(1)
	s.close()
def conn_string(f, g, a):
	try:
		first_line = g.split("\n")[0]

		u = first_line.split(" ")[1]
		
		http_pos = u.find("://")
		print("[!] " + u + " accessible.")
	
		if(http_pos == 4):
			print("[*] Running on Port 80.")
			p = 80
		elif(http_pos == -1):
			print("[*] Running on Port 443.")
			p = 443
		proxy_server(u, p, f, g, a)
	except Exception, e:
		pass
def proxy_server(sw, port, f, g, a):
	ws = sw.split(":")[0]
	sp = sw.split(":")[1]
	print("[*] Streaming Website: " + ws + ":" + sp)
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		try:
			wh = socket.gethostbyname(ws)
		except socket.gaierror:
			print("404: Error Host.")
			sys.exit()
			
		print("[!] Host: 200 | " + wh)
		
		c.connect((wh, 80))
		CRLF = ("\r\n\r\n")
		
		#Carrier Return, Line Feed
		
		try:
			c.send("GET / HTTP/1.0%s" % (CRLF))
		except socket.error:
			print("404: Send Error.")
    			sys.exit()
			
		dta = (1)
		
		while(dta):
			if(len(c.recv(4096)) > 0):
				dar = float(len(c.recv(4096)))
				dar = float(dar / 4096)
				dar = "%.3s" % (str(dar))
				dar = "%s KB" % (dar)
				print("[*] Request Done: %s => %s <=" % (str(a[0]),str(dar)))
				f.send(c.recv(4096))
				f.send("Hello World!")
				print("[DATA]: " + repr(f.recv(4096)))
				continue
			else:
				c.send(c.recv(4096))
				
		c.close()
		f.close()
	except socket.error, (value, message):
		c.close()
		f.close()
		sys.exit(1)
start(lp)
