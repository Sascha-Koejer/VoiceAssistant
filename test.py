import os
import sys
import json
from json.decoder import JSONDecodeError
import spotipy
import spotipy.util as util

username = "koejer.sascha@gmail.com"
scope = "user-read-private user-read-playback-state user-modify-playback-state"
client_id = "1222d7149c7c49d28a567e5c856f3a6f"
client_secret = "a0ad652efc8c4fe0935e5d531f224139"
redirect_uri = "http://localhost/"

token  = util.prompt_for_user_token(username, scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)

    devices = sp.devices()
    print(json.dumps(devices, sort_keys=True, indent=4))
    deviceID = devices["devices"][0]["id"]

else:
    print ("Can't get token for", username)


def playSong(song):
    result = sp.search(song, 1, 0,"track")
    print(json.dumps(result, sort_keys=True, indent=4))
    trackURI = [result["tracks"]["items"][0]["uri"]]
    sp.start_playback(deviceID, None, trackURI)

