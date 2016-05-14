'''
Created on Apr 18, 2016

@author: Roman
'''

import json

def pretty_print(response):
    print(json.dumps(response, sort_keys=True, indent=4))
