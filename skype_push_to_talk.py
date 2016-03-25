#!/usr/bin/python2
"""
The MIT License (MIT)

Copyright (c) 2016 Paul Batty

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq
import dbus

disp = None
bus = None
skype = None

def handler(reply):
    """ This function is called when a xlib event is fired """
    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, disp.display, None, None)
       
       # KEYCODE IS FOUND USERING event.detail
       # 8 is mouse 4 replace with own
        if event.detail == 8: 
            command = "MUTE ON"
            if skype.Invoke('GET MUTE') == "MUTE ON":
                command = "MUTE OFF"
            skype.Invoke(command)
            #if event.type == X.KeyPress:
                # BUTTON PRESSED
            #    print "pressed"
            #elif event.type == X.KeyRelease:
                # BUTTON RELEASED
            #    print "released"

# get skype
bus = dbus.SessionBus()
skype = bus.get_object('com.Skype.API', '/com/Skype')

#connect to skype
skype.Invoke('NAME skype-linux-ptt')
skype.Invoke('PROTOCOL 5')

# get current display
disp = Display()
root = disp.screen().root

# Monitor keypress and button press
ctx = disp.record_create_context(
        0,
        [record.AllClients],
        [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }])
disp.record_enable_context(ctx, handler)
disp.record_free_context(ctx)

while 1:
    # Infinite wait, doesn't do anything as no events are grabbed
    event = root.display.next_event()
