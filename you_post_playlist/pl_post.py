# -*- encoding: utf-8
import os, fnmatch
import argparse
import httplib2
import webbrowser
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import xml.etree.cElementTree as ET
from flask import Flask, request
from multiprocessing import Process


CONFIG_FILE = 'config.json'
REDIRECT_URI = "http://localhost:65010/auth_callback"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0
    YOUTUBE_INSERT_PLAYLIST = 'https://www.googleapis.com/youtube/v3/playlists'
    """
OAUTH2_FNAME = 'you-oauth2.json'


app = Flask(__name__)
@app.route('/auth_callback')
def auth_redir():
    error = request.args.get('error', '')
    if error:
        text = '<P>Clear you-oauth2.json file , error %s</P>'% error
    code = request.args.get('code', None)
    if code:
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
        ).execute()
    for video in search_response['items']:
        print(video['snippet']['title'])
    return search_response['items'][0]['id']['videoId']


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
            }
        }
    ).execute()
    return add_video_request


def main():
    p = argparse.ArgumentParser(description='Symbols image generator')
    p.add_argument('-d','--dir', default='playlists', help='Playlist directory, default=./playlist')
    p.add_argument('-f','--files', default=['*.pl'], help='Playlist files name *.pl, default=all files', nargs='+')
    args = p.parse_args()

    file_list = find(args.files, args.dir)

    youtube = get_authenticated_service()
    #youtube=True
    if youtube:
        for pl_file in file_list:
            tree = ET.ElementTree(file=pl_file)
            root = tree.getroot()
            #playlistID = 'PL_m6k8y2vgaKt2-vxbEI3E-5BiPPaMLhO'
            playlistID = ins_playlist(
                    youtube,
                    title=root.find('title').text,
                    description=root.find('description').text
                )
            films = root.find('films')
            for film in films:
                print(film.text)
                v_id = search_video(youtube, title=film.text)
                add_video_to_playlist(youtube, v_id, playlistID)
    return 0


def get_authenticated_service():
    if not os.path.exists(OAUTH2_FNAME):
        open(OAUTH2_FNAME, 'a').close()
    storage = Storage("you-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        server = Process(target=app.run, kwargs={'debug': True, 'port': 65010})
        server.start()
        flow = flow_from_clientsecrets(os.path.abspath(CONFIG_FILE),
            scope=YOUTUBE_SCOPE,
            message=MISSING_CLIENT_SECRETS_MESSAGE,
            redirect_uri=REDIRECT_URI
        )

        auth_uri = flow.step1_get_authorize_url()
        webbrowser.open_new(auth_uri)
        code = raw_input('code  из строки:')
        server.terminate()
        credentials = flow.step2_exchange(code)
        storage.put(credentials)

    if credentials:
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                http=credentials.authorize(httplib2.Http()))
    else:
        return None


if __name__ == '__main__':
    main()

