#!/usr/bin/env python

#pip install -U selenium
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        #print(self.command())
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        parsed =  urlparse.urlparse(self.path)

        #url="https://www.youtube.com/embed/hht6b6LprHg?autoplay=1&rel=0"
        #os.system("chromium-browser --kiosk " + url)
        
        # Send message back to client
        query =  urlparse.parse_qs(parsed.query)
        print(str(query))
        videoID=(query['video'][0])

        if videoID=="x":
            display_standby(False)
            print("killen ...")
            self.wfile.write(bytes("beenden", "utf8"))
            PROCNAME = "chromium-browser"
            os.system("killall "+PROCNAME)
        elif videoID!="":
            display_standby(True)
            #erstmal beenden...
            PROCNAME = "chromium-browser"
            os.system("killall "+PROCNAME)
            #... starten
            url="https://www.youtube.com/embed/" + videoID + "?autoplay=1&rel=0"
            os.system("chromium-browser --kiosk " + url)
                    
        # Write content as utf-8 data
        self.wfile.write(bytes("OK", "utf8"))

        return

def display_standby(standby):
    if standby:
      PROCNAME = "vcgencmd display_power 1"
    else:
      PROCNAME = "vcgencmd display_power 0"

    os.system(PROCNAME)

def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('192.168.178.67', 8080)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()
