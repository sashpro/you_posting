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
from multiprocessing import Process
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
@app.route('/auth_callback')
def auth_redir():
    # error = request.args.get('error', '')
    # global credential
    # if error:
    #     credential = CRED_ERROR
    #     return "Error: " + error
    #
    code = request.args.get('code', None)
    # if code:
    #     credentials = flow.step2_exchange(code)
    #
    #     storage = Storage("you-oauth2.json")
    #     storage.put(credentials)
    #     credential = CRED_READY
    #     # get_token(code)
    text = '<P>Copy code in console - </P>%s'
    return text % code


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
        {
            "kind": "youtube#searchResult",
            "snippet": {

                "title": kwargs.get('title',''),
            },
        }
        ).execute()
    print "search list: %s" % search_response


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
                search_video(youtube, title=film.text)
            add_video_to_playlist(youtube, 'hCcU3KjTdEU', playlistID)


def get_authenticated_service(args):

    storage = Storage("you-oauth2.json")
    #credentials = storage.get()

    #if credentials is None or credentials.invalid:
    global flow
    flow = flow_from_clientsecrets(os.path.abspath(CONFIG_FILE),
                                   scope=YOUTUBE_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE,
                                   redirect_uri=REDIRECT_URI)

    auth_uri = flow.step1_get_authorize_url()
    webbrowser.open_new(auth_uri)
    code = raw_input('code  из строки:')
    credentials = flow.step2_exchange(code)

    if credentials:
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                http=credentials.authorize(httplib2.Http()))
    else:
        return None


if __name__ == '__main__':
    server = Process(target=app.run, kwargs={'debug': True, 'port': 65010})
    server.start()
    main()




# CLIENT_ID = "p-jcoLKBynTLew"
# CLIENT_SECRET = "gko_LXELoV07ZBNUXrvWZfzE3aI"
# REDIRECT_URI = "http://localhost:65010/reddit_callback"
#
# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# def homepage():
#     text = '<a href="%s">Authenticate with reddit</a>'
#     return text % make_authorization_url()
#
# def make_authorization_url():
#     # Generate a random string for the state parameter
#     # Save it for use later to prevent xsrf attacks
#     from uuid import uuid4
#     state = str(uuid4())
#     save_created_state(state)
#     params = {"client_id": CLIENT_ID,
#               "response_type": "code",
#               "state": state,
#               "redirect_uri": REDIRECT_URI,
#               "duration": "temporary",
#               "scope": "identity"}
#     import urllib
#     url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
#     return url
#
# # Left as an exercise to the reader.
# # You may want to store valid states in a database or memcache,
# # or perhaps cryptographically sign them and verify upon retrieval.
# def save_created_state(state):
#     pass
# def is_valid_state(state):
#     return True
#
# def main():
#     print('main')
#     while True:
#         pass
#
# if __name__ == '__main__':
#     app.run(debug=True, port=65010)
#     main()