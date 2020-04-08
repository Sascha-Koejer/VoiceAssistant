import os
import sys
import json
from json.decoder import JSONDecodeError
import spotipy
import spotipy.util as util
import time
from configparser import  ConfigParser

settings_path = os.path.expandvars(R"C:\Users\$USERNAME\Documents\VoiceAssistant\settings.ini")
config = ConfigParser()
config.read(settings_path)

username = config.get("Spotify", "username")
scope = "user-read-private user-read-playback-state user-modify-playback-state"
client_id = config.get("Spotify", "client_id")
client_secret = config.get("Spotify", "client_secret")
redirect_uri = "https://www.google.de"

token  = util.prompt_for_user_token(username, scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)

    devices = sp.devices()
    deviceID = config.get("Spotify", "device_id")

else:
    print ("Can't get token for", username)


def playSongFromArtist(track, artist):
    result = sp.search(q='artist:{} track:{}'.format(artist, track), limit = 1, offset = 0, type = "track")
    trackURI = [result["tracks"]["items"][0]["uri"]]
    sp.start_playback(deviceID, None, trackURI)

def playSong(track):
    result = sp.search(q='track:{}'.format(track), limit = 1, offset = 0, type = "track")
    trackURI = [result["tracks"]["items"][0]["uri"]]
    sp.start_playback(deviceID, None, trackURI)

def stopSong():
    sp.pause_playback()

def previousSong():
    sp.previous_track()

def change_device(newDeviceID):
    transfer_playback(newDeviceID, force_play=True)


