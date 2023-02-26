#!/usr/bin/env python

#pip install -U selenium
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os
import subprocess
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

        # Send message back to client
        query =  urlparse.parse_qs(parsed.query)
        print(str(query))
        videoID=(query['video'][0])
        #reboot=(query['reboot'][0])
        #url=(query['url'][0])
        
        #Browser beenden
        PROCNAME = "chromium-browse"
        os.system("killall "+PROCNAME)
        #VLC beenden
        PROCNAME = "vlc"
        os.system("killall "+PROCNAME)
        PROCNAME = "cvlc"
        os.system("killall "+PROCNAME)

        if videoID=="x":
            display_standby(False)
            print("killen ...")
            self.wfile.write(bytes("beenden", "utf8"))            
        elif videoID!="":
            display_standby(True)
            #erstmal beenden...
            PROCNAME = "chromium-browse"
            os.system("killall "+PROCNAME)
            
            #... starten
            if ".m3u8" in videoID:
                #VLC starten
                print("VLC starten...")
                #os.system("vlc  --fullscreen --no-embedded-video " + videoID)
                #os.system("vlc  --fullscreen " + videoID)
                command="/usr/bin/vlc --fullscreen " + videoID
                p = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
                #p = subprocess.Popen(["/usr/bin/vlc", "" + videoID], stdout=subprocess.PIPE)
                print("VLC läuft...")
            elif "https://" in videoID or "http://" in videoID:
                url=videoID
                os.system("chromium-browser --kiosk --autoplay-policy=no-user-gesture-required " + url + " &")
                print("fertig")
            else:
                #url="https://www.youtube.com/embed/" + videoID + "?autoplay=0&rel=0"
                url="https://www.youtube.com/embed/" + videoID + "?autoplay=0"
                print("starten ..." + url)
                os.system("chromium-browser --kiosk --autoplay-policy=no-user-gesture-required " + url + " &")
                print("fertig...")        
                    
        # Write content as utf-8 data
        self.wfile.write(bytes("OK", "utf8"))

        return

def display_standby(standby): #Display in Standby setzen
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
  print('**running server...')
  httpd.serve_forever()
 
 
run()

