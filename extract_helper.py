import spotipy
import pandas as pd
import psycopg2
import os

from sqlalchemy import create_engine
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET_ID = os.getenv('SPOTIFY_CLIENT_SECRET')

def spotify_extract_init():
    album_list = []
    spotify_redirect_url = "http://localhost:8000/callback"

    sp_connect = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET_ID,
        redirect_uri=spotify_redirect_url,
        scope="user-read-recently-played"
    ))

    data = sp_connect.current_user_recently_played(limit=50)
    print(data)

    if len(data) == 0:
        print("data not found")

    else:
        for row in data['items']:
            id_track = row['track']['id']
            name_track = row['track']['name']
            url_track = row['track']['external_urls']['spotify']
            popularity_track = row['track']['popularity']
            duration_ms_track = row['track']['duration_ms']
            album_id = row['track']['album']['id']
            artists_id = []
            for key, value in row.items():
                if key == "track":
                    for point in value['artists']:
                        artists_id.append(point['id'])

            played_at = row['played_at']
            # artist_id = row['track']['artists']
            # album_name = row['track']['album']['name']
            # album_url = row['track']['album']['external_urls']['spotify']
            # album_release_date = row['track']['album']['release_date']
            # album_total_tracks = row['track']['album']['total_tracks']

            album_elements = {
                'id_track': id_track,
                'name_track': name_track,
                'url_track': url_track,
                'popularity_track': popularity_track,
                'duration_ms_track': duration_ms_track,
                'album_id': album_id,
                'artists_id': artists_id,
                'played_at': played_at
                # 'album_name': album_name,
                # 'album_url': album_url,
                # 'album_release_date': album_release_date,
                # 'album_total_tracks': album_total_tracks
            }

            album_list.append(album_elements)

        album_df = pd.DataFrame.from_dict(album_list)

        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            print(album_df)

        # Borrar duplicados
        # album_df = album_df.drop_duplicates(subset=['album_id'])

        # Fechas
        # album_df['played_at'] = pd.to_datetime(album_df['played_at'], format='%Y-%m-%d %H:%m:%s')

        # print(album_df['played_at'])

        # fecha de carga, como conectarme a una base de datos postdre, subir codigo a github

spotify_extract_init()
