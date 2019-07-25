import spotipy
import spotipy.util as util
import json
import datetime
import re
import pyfy
from machine_learning import prediction
from flask import jsonify

result = list()

def mood(spt, recent):
        for i in recent['items']:
                date_played = json.dumps(i['played_at'], sort_keys=True, indent=2)
                today_date = str(datetime.date.today())

                if today_date in date_played:

                        track = i['track']
                        song_id = track['id']

                        track_info = spt.tracks_audio_features(song_id)
                        energy = track_info['energy']
                        valence = track_info['valence']
                        danceability = track_info['danceability']
                        tempo = track_info['tempo'] / 250
                        data = [energy, valence, danceability, 0.5, tempo]
                        mood = prediction(data)
                        result.append(mood)
        try:
                mood_number = max(set(result), key=result.count)
        except:
                mood_number = 4
        
        return mood_number