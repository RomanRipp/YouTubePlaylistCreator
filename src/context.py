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
        self._pbar.update(100)
        self._pbar.finish()
    
    def Update(self):
        if self._it > 100:
            self._it = 0
        else:
            self._it = self._it + 1
        self._pbar.update(self._it)

    def __init__(self):
        '''
        Constructor
        '''
        self._it = 0
        widgets = [Percentage(), Bar()]
        self._pbar = ProgressBar(widgets=widgets, maxval=100).start()
