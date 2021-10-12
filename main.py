import json
import requests
import time
from ctypes import addressof, cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
from pprint import pprint
import base64

from requests.models import to_key_val_list

# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = ''
REFRESH_TOKEN = ""
auth_str = bytes('{}:{}'.format(CLIENT_ID_HERE!!!!!!!!, CLIENT_SECRET HERE!!!!!!!!!), 'utf-8')
BASE64 = base64.b64encode(auth_str).decode('utf-8')




class Refresh:
    
    def __init__(self):
        self.refresh_token = REFRESH_TOKEN
        self.base_64 = BASE64

    def refresh(self):

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": self.refresh_token},
                                 headers={"Authorization": "Basic " + self.base_64})

        response_json = response.json()
        print()
        print(response_json)
        print()

        return response_json["access_token"]








def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
    	"id": track_id,
    	"track_name": track_name,
    	"artists": artist_names,
    	"link": link
    }

    return current_track_info

def getcurrentvolume():
    # Get current volume 
    currentVolumeDb = volume.GetMasterVolumeLevel()
    return currentVolumeDb
def setcurrentvolume(val):
    volume.SetMasterVolumeLevel(val, None)
    # NOTE: -6.0 dB = half volume !

def mute():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "Spotify.exe":
            volume.SetMute(1, None)


def unmute():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == "Spotify.exe":
            volume.SetMute(0, None)

def main():
    refresher = Refresh()
    ACCESS_TOKEN = refresher.refresh()
    token_expires_counter = 0
    current_track_id = None
    ad_joined = False

    while True:
        token_expires_counter += 1
        if token_expires_counter > 3000:
            ACCESS_TOKEN = refresher.refresh()
            token_expires_counter = 0
        time.sleep(1)
        try:
            current_track_info = get_current_track(ACCESS_TOKEN)
            if current_track_info['id'] != current_track_id:
                pprint(current_track_info,indent=4,)
            current_track_id = current_track_info['id']
            if ad_joined:
                unmute()
                ad_joined = False
        except Exception as e:
            print(e)
            ad_joined = True
            mute()

if __name__ == '__main__':
    main()
