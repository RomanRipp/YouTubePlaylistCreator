'''
Created on Apr 13, 2016

@author: Roman
'''
import unittest
import os
import os.path as path
import preference_list as pl

class TestPreferenceList(unittest.TestCase):

    def Clean(self):
        file_name = 'channels.csv'
        if path.exists(file_name):
            os.remove(file_name)

    def test_initialization(self):
        self.Clean()
        preference_list = pl.PreferenceList() 
        self.assertTrue(len(preference_list._channels) == 0)
        self.Clean()        

    def test_add_channels_none(self):
        self.Clean()
        preference_list = pl.PreferenceList() 
        preference_list.AddChannels('')
        self.assertTrue(len(preference_list._channels) == 0)
        self.Clean()
        
    def test_add_channels_one(self):
        self.Clean()
        preference_list = pl.PreferenceList() 
        preference_list.AddChannels('The Verge')
        self.assertTrue(len(preference_list._channels) == 1)
        self.assertTrue(preference_list._channels[0] == 'The Verge')
        self.Clean()

    def test_add_channels_many(self):
        self.Clean()
        preference_list = pl.PreferenceList() 
        preference_list.AddChannels('The Verge; Motor Trend;Vice')
        self.assertTrue(len(preference_list._channels) == 3)
        self.assertTrue(preference_list._channels[0] == 'The Verge')
        self.assertTrue(preference_list._channels[1] == 'Motor Trend')
        self.assertTrue(preference_list._channels[2] == 'Vice')
        self.Clean()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAddChannel']
    unittest.main()