'''
Created on Apr 14, 2016

@author: Roman
'''

import os
import os.path as path
import httplib2
import oauth2client.file as a2cfile
import oauth2client.client as a2cclient
import oauth2client.tools as a2ctools
from apiclient.discovery import build
import json

import youtube_utilities as utils

class YouTubeApi(object):
    APPLICATION_NAME = 'youtube-recommender'
    SECRET_FILE = '../client_secret.json'
    SCOPE = 'https://www.googleapis.com/auth/youtube'
    YOUTUBE_API_VERSION = 'v3'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0
    
    To make this sample run you will need to populate the client_secrets.json file
    found at:
    
       %s
    
    with information from the Developers Console
    https://console.developers.google.com/
    
    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       SECRET_FILE))
    
    PLAYLIST_NAME = 'Recommended Videos'
                
    def find_playlist(self, playlists, name):
        for item in playlists:
            if item['snippet']['title'] == name:
                self.user_playlist_cache = item
                return self.user_playlist_cache
        return None                    
    
    def find_user_playlist(self):
        user_playlists = self.get_user_playlists()
        return self.find_playlist(user_playlists, self.PLAYLIST_NAME)
            
    def get_user_playlists(self):
        if not self.user_playlist_cache:
            response = self.youtube.playlists().list(part='snippet', mine='true').execute()
            self.playlists_cache = response['items']
        return self.playlists_cache 
            
    def add_video_to_playlist(self, videoID, playlistID):
        return self.youtube.playlistItems().insert(part="snippet",
        body={
                'snippet': {
                  'playlistId': playlistID, 
                  'resourceId': {
                          'kind': 'youtube#video',
                      'videoId': videoID
                    }
                }
        }
    ).execute()
    
    def remove_item_from_playlist(self, itemId):
        return self.youtube.playlistItems().delete(id=itemId).execute()
    
    def add_videos_to_playlist(self, videos):
        playlist = self.find_user_playlist()
        if playlist is None:
            self.create_playlist()
        for video in videos:
            if video is not None:
                self.add_video_to_playlist(video['contentDetails']['videoId'], playlist['id'])
            
    def create_playlist(self):
        response = self.find_user_playlist()
        if response is None:
            response = self.youtube.playlists().insert(
                part="snippet,status",
                body=dict(snippet=dict(title=self.PLAYLIST_NAME,
                                       description="A private playlist created with the YouTube API v3"),
                          status=dict(privacyStatus="private"))).execute()
        self.user_playlist_cache = response
        return response
    
    def delete_watched_videos(self, playlist):
        user_channel = self.find_user_channel()
        watched_playlist = user_channel['items'][0]['contentDetails']['relatedPlaylists']['watchHistory']
        video_items_to_watch = self.find_all_video_items(playlist['id'])
        watched_video_items = self.find_all_video_items(watched_playlist)
        self.watched_video_items_cache = watched_video_items
        for video_to_watch in video_items_to_watch:
            for watched_video in watched_video_items:
                if video_to_watch['contentDetails']['videoId'] == watched_video['contentDetails']['videoId']:
                    result = self.remove_item_from_playlist(video_to_watch['id']);
                    utils.pretty_print(result)
                    
        
    def find_channel(self, name):
        return self.youtube.channels().list(forUsername=name, part="contentDetails").execute()

    def find_user_channel(self):
        return self.youtube.channels().list(mine=True, part="contentDetails").execute()        


    def find_videos(self, playlistId, videosCountLimit):
        videos = self.youtube.playlistItems().list(
                        playlistId=playlistId, 
                        maxResults=50, 
                        part="contentDetails").execute()
        video_items = self.filter(videos['items'])
        videosCountLimit = videosCountLimit - len(video_items)
         
        while len(video_items) < videosCountLimit and 'nextPageToken' in videos:
            videos = self.youtube.playlistItems().list(
                            playlistId=playlistId, 
                            maxResults=50, 
                            pageToken=videos['nextPageToken'],
                            part="contentDetails").execute()
            video_items.extend(self.filter(videos['items']))
        return video_items
    
    
    def find_all_video_items(self, playlistId):
        pageVideos = self.youtube.playlistItems().list(
                        playlistId=playlistId, 
                        maxResults=50, 
                        part="contentDetails").execute()
                        
        allVideos = pageVideos['items']
        while 'nextPageToken' in pageVideos:
            pageVideos = self.youtube.playlistItems().list(
                        playlistId=playlistId, 
                        maxResults=50, 
                        pageToken=pageVideos['nextPageToken'],
                        part="contentDetails").execute()
            allVideos.extend(pageVideos['items'])
        return allVideos
    
    def add_videos_from_channels(self, channel_names):
        for item in channel_names:
            channel = self.find_channel(item)
            if channel is None: 
                raise NotImplemented            
            for items in channel['items']:
                uploads_playlist = items['contentDetails']['relatedPlaylists']['uploads']
            channel_videos = self.find_videos(uploads_playlist, 10)
            self.add_videos_to_playlist(channel_videos)
    
    def filter(self, video_items):
        if self.watched_video_items_cache is None:
            user_channel = self.find_user_channel()
            watched_playlist = user_channel['items'][0]['contentDetails']['relatedPlaylists']['watchHistory']
            self.watched_video_items_cache = self.find_all_video_items(watched_playlist)
             
        if self.user_playlist_items_cache is None:
            if self.user_playlist_cache is None:
                self.find_user_playlist()
            self.user_playlist_items_cache = self.find_all_video_items(self.user_playlist_cache['id'])
            
        filtered_video_items = []
        for video_item in video_items:
            isNew = True
            for watched_video_item in self.watched_video_items_cache:
                if watched_video_item['contentDetails']['videoId'] == video_item['contentDetails']['videoId']:
                    isNew = False;
                    break
                    
            for playlist_video_item in self.user_playlist_items_cache:
                if playlist_video_item['contentDetails']['videoId'] == video_item['contentDetails']['videoId']: 
                    isNew = False;
                    break
            
            if isNew:
                filtered_video_items.append(video_item)
                
        return filtered_video_items
    
    def populate_playlist(self, preffered_channels):
        if self.user_playlist_cache is None:
            self.find_user_playlist()
#         self.delete_watched_videos(self.user_playlist_cache)
        self.add_videos_from_channels(preffered_channels)
            
    def get_credentials(self, args):
        home_dir = path.expanduser('~')    
        credentials_dir = path.join(home_dir, '.credentials')
        if not path.exists(credentials_dir):
            os.makedirs(credentials_dir)
        credential_path = path.join(credentials_dir, 'youtube-recomender.json')
        store = a2cfile.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = a2cclient.flow_from_clientsecrets(self.SECRET_FILE, self.SCOPE, self.MISSING_CLIENT_SECRETS_MESSAGE)
            flow.user_agent = self.APPLICATION_NAME
            credentials = a2ctools.run_flow(flow, store, args)
        
        self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, 
                     self.YOUTUBE_API_VERSION, 
                     http=credentials.authorize(httplib2.Http()))        

    def __init__(self):
        '''
        Constructor
        '''
        self.playlists_cache = None
        self.user_playlist_cache = None
        self.user_playlist_items_cache = None
        self.watched_video_items_cache = None
        