import streamlit as st
import json
import time
from dotenv import load_dotenv
import os
import base64
from requests import post,get
from googleapiclient.discovery import build

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
youtube_api = os.getenv("YOUTUBE_API")


def get_song_names_from_link(playlist_id):
    song_list=[]

    youtube = build('youtube', 'v3', developerKey=youtube_api)

    # Request playlist items
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    response = request.execute()

    # Print playlist items and attempt to extract song names
    for item in response['items']:
        title = item['snippet']['title']

        if "|" in title:
            song_name, artist = title.split("|", 1)
        elif "-" in title:
            song_name, artist = title.split("|", 1)
        else:
            song_name = title

        song_list.append(song_name)
        
        print(f'Song Name: {song_name}')
    return song_list


### main ###

playlist_id = "PLoxJJjc_pjUFBdHiExeN0ywPJf-aAfFhG"


st.write(playlist_id)