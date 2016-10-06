import sys
import os

import urlparse, urllib
import time

from threading import Thread

import vlc
from vlc import *

def path2url(path):
    return urlparse.urljoin(
      'file:', urllib.pathname2url(path))
def getVideoPath(video):
    return path2url(os.path.dirname(os.path.abspath(__file__)) + "\\Videos\\" + video)

change = False

order_i = 0

from order import order

def end_callback(event):
    global change
    print('End of media stream (event %s)' % event.type)
    change = True

def quit_app():
    """Stop and exit"""
    sys.exit(0)

def threaded_function(arg):
    global change
    global order_i
    global order
    p = None
    i = None
    
    if len(order) < 0:
        return
    
    i=vlc.Instance('--fullscreen')
    p=i.media_player_new()
    event_manager = p.event_manager()
    event_manager.event_attach(EventType.MediaPlayerEndReached, end_callback)
    p.set_fullscreen(True)
    
    while True:
        if order_i + 1 > len(order):
            return
        
        path = order[order_i]
        print(getVideoPath(path))
        m=i.media_new(getVideoPath(path))
        p.set_media(m)
        p.play()
        while change is False:
            2+2
        print("Changing..")
        order_i = order_i + 1
        change = False
    
    
if __name__ == "__main__":
    #p=vlc.MediaPlayer('file:///tmp/foo.avi')
    
    thread = Thread(target = threaded_function, args = (getVideoPath("1.MP4"), ))
    thread.start()
    
    
    
    #thread.join()
    #sys.exit(0)
    while True:
        
    #time.sleep(4)
    #sys.exit(0)
    """
    from kidect import kidect
    running = True
    ki = kidect()
    ki.init()

    while running:
        ki.update()
        if ki.detected():
            sys.stdout.write('!')
        else:
            sys.stdout.write('.')

    ki.close()
    """