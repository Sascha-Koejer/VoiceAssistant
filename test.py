import os
import sys
import json
from json.decoder import JSONDecodeError
import spotipy
import spotipy.util as util
import webbrowser

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
    deviceID = devices["devices"][4]["id"]

    result = sp.search("Hold My Girl", 1, 0,"track")
    print(json.dumps(result, sort_keys=True, indent=4))
    print(result["tracks"]["items"][0])
    trackURI = ['spotify:track:42bbDWZ8WmXTH7PkYAlGLu']
    sp.start_playback(deviceID, None, trackURI)
    
else:
    print ("Can't get token for", username)



#print(json.dumps(user, sort_keys=True, indent=4))
 #   result = sp.search("YTITTY", 1, 0,"artist")
  #  print(json.dumps(result, sort_keys=True, indent=4))
   # artist = result["artists"]["items"][0]
    #print(artist["name"])
    #webbrowser.open(artist["images"][0]["url"])