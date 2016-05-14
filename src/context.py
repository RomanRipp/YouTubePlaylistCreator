'''
Created on Apr 13, 2016

@author: Roman
'''

from progressbar import ProgressBar, Percentage, Bar

class Context(object):
    '''
    classdocs
    '''
    def Release(self):
        self._pbar.update(self.max_val)
        self._pbar.finish()
    
    def Update(self, new_val):
        new_val % self.max_val
        self._it = new_val
        self._pbar.update(self._it)

    def ShowMessage(self, msg):
        print(msg)

    def __init__(self, max_val):
        '''
        Constructor
        '''
        self._it = 0
        self.max_val = max_val
        widgets = [Percentage(), Bar()]
        self._pbar = ProgressBar(widgets=widgets, maxval=max_val).start()
