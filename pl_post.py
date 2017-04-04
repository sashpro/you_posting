# -*- encoding: utf-8
import os, fnmatch
import argparse
import sys
#import request
import httplib2
import webbrowser
from wsgiref.simple_server import make_server
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import socket               # Import socket module
import xml.etree.cElementTree as ET

from flask import Flask, request
from multiprocessing import Process, Manager
# CLIENT_ID = "p-jcoLKBynTLew"
# CLIENT_SECRET = "gko_LXELoV07ZBNUXrvWZfzE3aI"
CONFIG_FILE = 'config.json'
REDIRECT_URI = "http://localhost:65010/auth_callback"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
# YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0
    YOUTUBE_INSERT_PLAYLIST = 'https://www.googleapis.com/youtube/v3/playlists'
    """
CRED_ERROR = 'E'
CRED_READY = 'R'

flow = None
credential = None


app = Flask(__name__)
#server = Process(target=app.run, kwargs={'debug': True, 'port': 65010})
#server.start()
@app.route('/auth_callback')
def auth_redir():
    error = request.args.get('error', '')
    # global credential
    if error:
        text = '<P>Clear you-oauth2.json file , error %s</P>'% error
    #     credential = CRED_ERROR
    #     return "Error: " + error
    #
    code = request.args.get('code', None)
    if code:
    #     global flow
    #     print(flow)
    #     credentials = flow.step2_exchange(code)
    #
    #     storage = Storage("you-oauth2.json")
    #     storage.put(credentials)
    #     #credential = CRED_READY
    #     # get_token(code)
        text = '<P>Copy code in console - </P>%s'% code
    return text


def find(pattern_files, path):
    """
    looking filename for file pattern
    """
    result = []
    dir_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for pat_name in pattern_files:
        for file_name in dir_files:
            if fnmatch.fnmatch(file_name, pat_name):
                result.append(os.path.join(os.path.abspath(path), file_name))
    return result


def search_video(youtube, **kwargs):
    search_response = youtube.search().list(
        q=kwargs.get('title'),
        part='snippet',
        maxResults=1,
        type='video',
        order='viewCount'
        # kind="youtube#searchResult"
            # "snippet": {
            #
            #     "title": kwargs.get('title'),
            # },

        ).execute()
    for video in search_response['items']:
        print(video['snippet']['title'])
    #print(search_response['items'][1]['id']['videoId'])
    return search_response['items'][0]['id']['videoId']

    # for video in search_response['items']:
    #     print "search list: %s" % video['id']


def ins_playlist(youtube, **kwargs):
    playlists_insert_response = youtube.playlists().insert(
        part="snippet,status",
        body=dict(
            snippet=dict(
                title=kwargs.get('title',''),
                description=kwargs.get('description','')
            ),
            status=dict(
                privacyStatus="private"
            )
        )
    ).execute()
    print "New playlist id: %s" % playlists_insert_response["id"]
    return playlists_insert_response["id"]


def add_video_to_playlist(youtube, videoID, playlistID):
    add_video_request=youtube.playlistItems().insert(
        part="snippet",
        body={
            'snippet': {
              'playlistId': playlistID,
              'resourceId': {
                      'kind': 'youtube#video',
                  'videoId': videoID
                }
            #'position': 0
            }
        }
    ).execute()


def main():
    p = argparse.ArgumentParser(description='Symbols image generator')
    p.add_argument('-d','--dir', default='playlists', help='Playlist directory, default=./playlist')
    p.add_argument('-f','--files', default=['*.pl'], help='Playlist files name *.pl, default=all files', nargs='+')
    args = p.parse_args()

    file_list = find(args.files, args.dir)
    print(file_list)

    youtube = get_authenticated_service(args)
    #youtube=True
    if youtube:
        for pl_file in file_list:
            tree = ET.ElementTree(file=pl_file)
            root = tree.getroot()
            playlistID = 'PL_m6k8y2vgaKt2-vxbEI3E-5BiPPaMLhO'
            # ins_playlist(
                # youtube,
                # title=root.find('title').text,
                # description=root.find('description').text
                # )
            films = root.find('films')
            for film in films:
                print(film.text)
                v_id = search_video(youtube, title=film.text)
                add_video_to_playlist(youtube, v_id, playlistID)
    return 0


def get_authenticated_service(args):

    storage = Storage("you-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        global flow
        flow = flow_from_clientsecrets(os.path.abspath(CONFIG_FILE),
                                       scope=YOUTUBE_SCOPE,
                                       message=MISSING_CLIENT_SECRETS_MESSAGE,
                                       redirect_uri=REDIRECT_URI)

        auth_uri = flow.step1_get_authorize_url()
        webbrowser.open_new(auth_uri)
        code = raw_input('code  из строки:')
        credentials = flow.step2_exchange(code)
        storage.put(credentials)

    if credentials:
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                http=credentials.authorize(httplib2.Http()))
    else:
        return None


if __name__ == '__main__':
    #code = Manager.Value('s', '')

    print('start_server')
    main()

