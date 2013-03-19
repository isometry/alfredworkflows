#-*- coding: utf-8 -*-
# trailer.alfredworkflow, v0.1
# Robin Breathe, 2013

import alfred
import json
import re
import requests
import requests_cache

from os import path
from time import time

_MAX_RESULTS=36
_TRAILER_URI='http://trailers.apple.com/trailers/home/scripts/quickfind.php?callback=results&q='

def complete(query, maxresults=_MAX_RESULTS):
    pass
