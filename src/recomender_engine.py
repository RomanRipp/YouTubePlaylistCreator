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
        
        youtube = yt.YouTubeApi()
        youtube.get_credentials(self.args)
        if self.args.updateplaylist:
            channel_list = ['theverge', 'motortrend', 'voxdotcom']
            youtube.create_playlist()
            youtube.populate_playlist(channel_list)
        elif self.args.cleanplaylist:
            if youtube.has_recomender_playlist():
                playlist = youtube.find_user_playlist()
                youtube.delete_watched_videos(playlist)
        else:
            raise NotImplemented
        
        print('Succsess')
        
    def __init__(self, args):
        '''
        Constructor
        '''
        self.args = args