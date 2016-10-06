import sys
import os

import urlparse, urllib
import time

from threading import Thread

import vlc
from vlc import *
import datetime

def path2url(path):
    return urlparse.urljoin(
      'file:', urllib.pathname2url(path))
def getVideoPath(video):
    return path2url(os.path.dirname(os.path.abspath(__file__)) + "\\Videos\\" + video)

change = False
order_i = 0
isRunning = True
from order import order

def end_callback(event):
    global change
    print('End of media stream (event %s)' % event.type)
    change = True

def quit_app():
    """Stop and exit"""
    #sys.exit(0)
    global isRunning
    isRunning = False

isVlcThreadRunning = False
    
def threaded_function(arg):
    global change
    global order_i
    global order
    global isVlcThreadRunning
    p = None
    i = None
    isVlcThreadRunning = True
    
    if len(order) < 0:
        return
    
    i=vlc.Instance('--fullscreen')
    p=i.media_player_new()
    event_manager = p.event_manager()
    event_manager.event_attach(EventType.MediaPlayerEndReached, end_callback)
    p.set_fullscreen(True)
    
    while isVlcThreadRunning:
        if order_i + 1 > len(order):
            continue
        
        path = order[order_i]
        print(getVideoPath(path))
        m=i.media_new(getVideoPath(path))
        p.set_media(m)
        p.play()
        while change is False and isVlcThreadRunning is True:
            2+2
        print("Changing..")
        order_i = order_i + 1
        change = False
def replay():
    global order_i
    order_i = 0

def isFinished():
    global order_i
    global order
    return order_i + 1 > len(order)

def getTimeDifferenceFromNow(TimeStart, TimeEnd):
    timeDiff = TimeEnd - TimeStart
    return timeDiff.total_seconds()
    
if __name__ == "__main__":
    global isRunning
    global isVlcThreadRunning
    thread = Thread(target = threaded_function, args = (getVideoPath("1.MP4"), ))
    thread.start()
    
    try:
        from msvcrt import getch
    except ImportError:
        import termios
        import tty

        def getch():  # getchar(), getc(stdin)  #PYCHOK flake
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            return ch
    
    
    keybindings = {
        'q': quit_app
    }
    
    from kidect import kidect
    running = True
    ki = kidect()
    ki.init()
    
    lastKinectData = datetime.datetime.now()
    
    while isRunning:
        
        if not isFinished():
            print("/")
        else:
            timeDifference = getTimeDifferenceFromNow(lastKinectData, datetime.datetime.now())
            #print(timeDifference)
            if timeDifference < 5:
                replay()
                #quit_app()
            else:
                quit_app()
        
        ki.update()
        if ki.detected():
            lastKinectData = datetime.datetime.now()
            sys.stdout.write('!')
        else:
            sys.stdout.write('.')
        
        
        
        k = ""#getch()
        if k in keybindings:
            keybindings[k]()
            
    ki.close()
    isVlcThreadRunning = False