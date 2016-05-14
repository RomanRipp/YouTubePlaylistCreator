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
        if self.pbar is not None:
            self.pbar.update(self.max_val)
            self.pbar.finish()
    
    def Update(self, new_val):
        if self.pbar is not None:
            new_val % self.max_val
            self.it = new_val
            self.pbar.update(self.it)

    def ShowMessage(self, msg):
        print(msg)

    def __init__(self, max_val):
        '''
        Constructor
        '''
        self.it = 0
        self.pbar = None
        self.max_val = max_val
        
        if max_val > 0:
            widgets = [Percentage(), Bar()]
            self.pbar = ProgressBar(widgets=widgets, maxval=max_val).start()
