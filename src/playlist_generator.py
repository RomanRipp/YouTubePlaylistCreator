'''
Created on Apr 13, 2016

@author: Roman
'''
import sys
from oauth2client import tools

import recomender_engine as re

def CreateYouTubePlaylist(args):
    recomender = re.Recomender(args)
    recomender.recommend()

def main(argv):
    flags = None
    try:
        import argparse
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        parser.add_argument('--addchannel', '-a', help='Adds channel(s) to preferences list. Separate channels with \':\'.', type=str, required=False)
        parser.add_argument('--delchannel', '-d', help='Removes channel(s) from preferences list. Separate channels with \':\'.', type=str, required=False)
        parser.add_argument('--shuffle', '-s', help='Shuffles playlist content', type=str, required=False)
        parser.add_argument('--sort', '-S', help='Sorts playlist based on order of channels in channel list', type=str, required=False)
        flags = parser.parse_args()
    except ImportError:
        print("Failed to parse input") 
    
    if flags:
        if flags.addchannel or flags.delchannel:
            play_list = pl.PreferenceList()
            play_list.AddChannels(flags.addchannel)
            play_list.RemoveChannels(flags.delchannel)
        elif flags.shuffle:
            raise NotImplemented
        elif flags.sort:
            raise NotImplemented
        else:
            CreateYouTubePlaylist(flags)
    
    print('Done')
    
if __name__ == '__main__':
    main(sys.argv[1:])