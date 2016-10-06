from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

class kidect(object):
    def __init__(self):
        self._done = False
        self._bodies = None
        self._detected = False
    
    def init(self):
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body)

    def update(self):
        if self._kinect.has_new_body_frame(): 
            self._bodies = self._kinect.get_last_body_frame()
        self._detected = False
        
        if self._bodies is not None: 
            for i in range(0, self._kinect.max_body_count):
                body = self._bodies.bodies[i]
                if not body.is_tracked: 
                    continue 
                self._detected = True
    
    def detected(self):
        return self._detected
    
    def close(self):
        # Close the Kinect sensor
        self._kinect.close()
