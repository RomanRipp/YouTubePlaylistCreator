'''
Created on Apr 14, 2016

@author: Roman
'''

import preference_list as pl
import youtube as yt

class Recomender(object):
    '''
    classdocs
    '''
    def recommend(self):
        #preference = pl.PreferenceList()
        #channel_list = preference.ReadChannelsFromFile('channels.csv')
        channel_list = ['theverge', 'motortrend', 'voxdotcom']
        youtube = yt.YouTubeApi()
        youtube.get_credentials(self.args)
        youtube.create_playlist()
        youtube.populate_playlist(channel_list)
        
    def __init__(self, args):
        '''
        Constructor
        '''
        self.args = args