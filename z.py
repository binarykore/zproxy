#! /usr/bin/env python
import socket, sys, re, ssl
from thread import *

try:
	lp = int(raw_input("[*] Listener:"))
except KeyboardInterrupt:
	print("\n[*] Disturbed!")
	sys.exit()

def start(lp):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(("0.0.0.0", lp))
		s.listen(25)
		print("[*] OK: 200")
	except Exception, e:
		print("[*] FAILED: 404")
		sys.exit(2)
	dta = 1
	while(dta):
		try:
			f, a = s.accept()
			d = f.recv(4096)
			start_new_thread(conn_string, (f, d, a))
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
	
		if(http_pos == 4):
			print("[*] Running on Port 80.")
			p = 80
		elif(http_pos == -1):
			print("[*] Running on Port 443.")
			p = 443
		proxy_server(u, f, g, a)
	except Exception, e:
		pass
def proxy_server(sw, f, g, a):
	ws = sw.split(":")[0]
	sp = sw.split(":")[1]
	#Carrier Return, Line Feed
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	http_p = 80
		
	try:
		wh = socket.gethostbyname(ws)
		print("[*] Streaming Website: " + wh + ":" + sp)
	except socket.gaierror:
		print("404: Error Host.")
		sys.exit()
	
	c.connect((wh, http_p))		
	
	try:
		print("[!] Host: " + wh + " | CRLF!")
		c.send("GET / HTTP/1.0\r\nHost: " + ws + "\r\nConnection: Keep-Alive\r\n\r\n")
	except socket.error:
		print("404: Send Error.")
		sys.exit()
	try:
		dta = (1)
		while(dta):
			if(len(c.recv(4096)) > 0):
				dar = float(len(c.recv(4096)))
				dar = float(dar / 4096)
				dar = "%.3s" % (str(dar))
				dar = "%s KB" % (dar)
				print("[*] Request Done: %s => %s <=" % (str(a[0]),str(dar)))
				f.send(c.recv(4096))#Bounce Back
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
