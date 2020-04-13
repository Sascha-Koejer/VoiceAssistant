import os
import sys
import json
from json.decoder import JSONDecodeError
import spotipy
import spotipy.util as util
import time
from configparser import  ConfigParser
import win32gui, win32con
import subprocess

settings_path = os.path.expandvars(R"C:\Users\$USERNAME\Documents\VoiceAssistant\settings.ini")
config = ConfigParser()
config.read(settings_path)

username = config.get("Spotify", "username")
scope = "user-read-private user-read-playback-state user-modify-playback-state"
client_id = config.get("Spotify", "client_id")
client_secret = config.get("Spotify", "client_secret")
deviceID = config.items("SpotifyDevices")[0][1]
redirect_uri = "https://www.google.de"

token = util.prompt_for_user_token(username, scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)
#hideWindow = win32gui.GetForegroundWindow()
#win32gui.ShowWindow(hideWindow , win32con.SW_HIDE)

if token:
    sp = spotipy.Spotify(auth=token)
    subprocess.Popen(os.path.expandvars(R"C:\Users\$USERNAME\AppData\Roaming\Spotify\Spotify.exe"))
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
    try:
        sp.previous_track()
        return True
    except BaseException as err:
        return False

def changeDevice(text):
    global deviceID
    for key in config["SpotifyDevices"]:
        if key in text:
            print(key)
            deviceID = config.get("SpotifyDevices", key)
            sp.transfer_playback(deviceID, force_play=True)

def changeVolume(change):
    currentVolume = sp.current_playback()["device"]["volume_percent"]
    if change == "+":
        sp.volume(currentVolume + 10, deviceID)
    elif change == "-":
        sp.volume(currentVolume - 10, deviceID)

def setVolume(change):
    if change == "eins":
        sp.volume(10, deviceID)
    elif change == "zwei":
        sp.volume(20, deviceID)
    elif change == "drei":
        sp.volume(30, deviceID)
    elif change == "vier":
        sp.volume(40, deviceID)
    elif change == "fünf":
        sp.volume(50, deviceID)
    elif change == "sechs":
        sp.volume(60, deviceID)
    elif change == "sieben":
        sp.volume(70, deviceID)
    elif change == "acht":
        sp.volume(80, deviceID)
    elif change == "neun":
        sp.volume(90, deviceID)
    elif change == "zehn":
        sp.volume(100, deviceID)
    

