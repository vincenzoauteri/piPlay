#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Google App Engine app"""
import webapp2
import re
import string

import subprocess
import sys, os
sys.path.append(os.path.dirname(__file__))

from handlers import *
from security import *

def play():
    bin_path = os.path.join(os.path.dirname(__file__), 'bin/')    
    videos_path = os.path.join(os.path.dirname(__file__), 'videos/')    
    proc = subprocess.Popen([bin_path + "omxplayer " + videos_path + "test.h264"], stdout=subprocess.PIPE, shell=True)
    logging.error("play!")
    logging.error(proc)
    (out, err) = proc.communicate()
    logging.error( out)
    logging.error( err)

routes = [
    ('/', FrontPageHandler),
    ('/explorer',ExplorerHandler),
    ('/player',VideoPlayerHandler),
    ('/remote',RemoteHandler)
    ]

application = webapp2.WSGIApplication(routes,
    debug=True)

"""
def application(environ,start_response):
    status = '200 OK' 
    output = 'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    play()
    return [output]
 """
     



