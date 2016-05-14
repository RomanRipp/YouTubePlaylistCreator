'''
Created on Apr 13, 2016

@author: Roman
'''

import sys
import csv
import os.path as path
import context as ct

class PreferenceList(object):
    '''
    classdocs
    '''
    
    def ReadChannelsFromFile(self, file_name):
        if not path.exists(file_name):
            return []
        context = ct.Context()
        channels = []
        channels_file = open(file_name, 'r')
        reader = csv.reader(channels_file, delimiter=' ', quotechar='|')
        for row in reader: 
            channels.append(row)
            context.Update()
        if channels_file and not channels_file.closed:
            channels_file.close()
        
        context.Release()
        return channels   
    
    def UpdateChannelsFile(self):
        self.WriteChannelsToFile(self._channels_file_name, self._channels)
    
    def WriteChannelsToFile(self, file_name, channels):
        context = ct.Context()
        channels_file = open(file_name, 'w')
        writer = csv.writer(channels_file, delimiter=' ',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for channel in channels:
            writer.writerow([channel])
            context.Update()
        if channels_file and not channels_file.closed:
            channels_file.close()
        context.Release()
    
    def AddChannels(self, names):
        context = ct.Context()
        if not names:
            return
        
        self._channels = self.ReadChannelsFromFile(self._channels_file_name)
        for name in names.split(';'):
            context.Update()
            name = name.strip()
            self._channels.append(name)
        context.Release()
        self.UpdateChannelsFile()
    
    def RemoveChannels(self, names):
        context = ct.Context()
        if not names:
            return
        
        self._channels = self.ReadChannelsFromFile(self._channels_file_name)
        for name in names.split(';'):
            context.Update()
            name = name.strip()
            if name in self._channels:
                self._channels.remove(name)
            else:
                print('Channel not found: '.join(name))
        context.Release()
        self.UpdateChannelsFile()

    def __init__(self):
        '''
        Constructor
        '''
        self._channels_file_name='channels.csv'
        self._channels = self.ReadChannelsFromFile(self._channels_file_name)
        
