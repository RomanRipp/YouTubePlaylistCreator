'''
Created on Apr 13, 2016

@author: Roman
'''
import sys
from oauth2client import tools

import recomender_engine as re
import preference_list as pl

def main(argv):
    flags = None
    try:
        import argparse
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        parser.add_argument('--addchannel', '-a', help='Adds channel(s) to preferences list. Separate channels with \':\'.', type=str, required=False)
        parser.add_argument('--delchannel', '-d', help='Removes channel(s) from preferences list. Separate channels with \':\'.', type=str, required=False)
        parser.add_argument('--updateplaylist', '-u', help='Pulls new videos from channels', action='store_true', required=False)
        parser.add_argument('--cleanplaylist', '-c', help='Removes watched videos from channel', action='store_true', required=False)
        flags = parser.parse_args()
    except ImportError:
        print("Failed to parse input") 
    
    if flags:
        if flags.addchannel or flags.delchannel:
            play_list = pl.PreferenceList()
            play_list.AddChannels(flags.addchannel)
            play_list.RemoveChannels(flags.delchannel)
        elif flags.updateplaylist or flags.cleanplaylist:
            recomender = re.Recomender(flags)
            recomender.recommend()
        else:
            parser.print_help()
    
if __name__ == '__main__':
    main(sys.argv[1:])