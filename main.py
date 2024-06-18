# import streamlit as st
# import json
# import time
# from dotenv import load_dotenv
# import os
# import base64
# from requests import post, get
# from googleapiclient.discovery import build

# load_dotenv()

# client_id = os.getenv("SPOTIFY_CLIENT_ID")
# client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
# youtube_api = os.getenv("YOUTUBE_API")

# def get_token():
#     auth_string = client_id + ":" + client_secret
#     auth_bytes = auth_string.encode("utf-8")
#     auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

#     url = "https://accounts.spotify.com/api/token"
#     headers = {
#         "Authorization": "Basic " + auth_base64,
#         "Content-Type": "application/x-www-form-urlencoded",
#     }
#     data = {"grant_type": "client_credentials"}

#     result = post(url, headers=headers, data=data)
#     json_result = json.loads(result.content)

#     token = json_result["access_token"]
#     return token

# def get_auth_header(token):
#     return {"Authorization": "Bearer " + token}

# def get_song_names_from_link(playlist_id):
#     song_list = []

#     youtube = build('youtube', 'v3', developerKey=youtube_api)

#     request = youtube.playlistItems().list(
#         part="snippet",
#         playlistId=playlist_id,
#         maxResults=50
#     )

#     response = request.execute()

#     for item in response['items']:
#         title = item['snippet']['title']

#         if "|" in title:
#             song_name, artist = title.split("|", 1)
#         elif "-" in title:
#             song_name, artist = title.split("-", 1)
#         else:
#             song_name = title

#         song_list.append(song_name.strip())

#     return song_list

# def extract_playlist_id(youtube_playlist_url):
#     playlist_id = ""

#     if youtube_playlist_url:
#         parts = youtube_playlist_url.split("list=")
#         if len(parts) > 1:
#             playlist_id = parts[1]

#     return playlist_id

# def search_song(token, song_name):
#     url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     params = {"q": song_name, "type": "track", "limit": 1}

#     response = get(url, headers=headers, params=params)
#     response_data = response.json()
    
#     if response_data["tracks"]["items"]:
#         return response_data["tracks"]["items"][0]["external_urls"]["spotify"]
#     return None


# ### main ###

# st.divider()

# token = get_token()

# st.write(""" #### Place your YouTube playlist link here 👇""")

# # input text field
# youtube_playlist_url = st.text_input("", placeholder="https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID", label_visibility="collapsed")
# st.divider()

# st.write(""" #### Place your Spotify playlist link here 👇""")

# # input text field
# spotify_playlist_url = st.text_input("", placeholder="https://open.spotify.com/playlist/YOUR_PLAYLIST_ID", label_visibility="collapsed")
# st.divider()

# # Extract playlist ID from URL
# playlist_id = extract_playlist_id(youtube_playlist_url)

# # submit button
# if st.button("submit"):
    
#     if playlist_id:
#         idx = 1
#         st.divider()
#         st.write("Song Names and Spotify Links:")
#         result = get_song_names_from_link(playlist_id)
#         for song_name in result:
#             song_url = search_song(token, song_name)
#             if song_url:
#                 st.write(f"{idx}. {song_name} - {song_url}")
#             else:
#                 st.write(f"{idx}. {song_name} - Not found on Spotify")
#             idx += 1
#     else:
#         st.warning("Please enter a valid YouTube Playlist URL.")


import streamlit as st
import json
import time
from dotenv import load_dotenv
import os
import base64
from requests import post, get
from googleapiclient.discovery import build

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
youtube_api = os.getenv("YOUTUBE_API")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)

    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_song_names_from_link(playlist_id):
    song_list = []

    youtube = build('youtube', 'v3', developerKey=youtube_api)

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    response = request.execute()

    for item in response['items']:
        title = item['snippet']['title']

        if "|" in title:
            song_name, artist = title.split("|", 1)
        elif "-" in title:
            song_name, artist = title.split("-", 1)
        else:
            song_name = title

        song_list.append(song_name.strip())

    return song_list

def extract_playlist_id(youtube_playlist_url):
    playlist_id = ""

    if youtube_playlist_url:
        parts = youtube_playlist_url.split("list=")
        if len(parts) > 1:
            playlist_id = parts[1]

    return playlist_id

def extract_spotify_playlist_id(spotify_playlist_url):
    playlist_id = ""

    if spotify_playlist_url:
        parts = spotify_playlist_url.split("/playlist/")
        if len(parts) > 1:
            playlist_id = parts[1].split("?")[0]

    return playlist_id

def search_song(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {"q": song_name, "type": "track", "limit": 1}

    response = get(url, headers=headers, params=params)
    response_data = response.json()
    
    if response_data["tracks"]["items"]:
        return response_data["tracks"]["items"][0]["uri"]
    return None

def add_songs_to_spotify_playlist(token, spotify_playlist_id, track_uris):
    url = f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks"
    headers = get_auth_header(token)
    data = json.dumps({"uris": track_uris})

    response = post(url, headers=headers, data=data)
    if response.status_code == 201:
        return True
    return False

### main ###

st.divider()

token = get_token()

st.write(""" #### Place your YouTube playlist link here 👇""")

# input text field
youtube_playlist_url = st.text_input("", placeholder="https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID", label_visibility="collapsed")
st.divider()

st.write(""" #### Place your Spotify playlist link here 👇""")

# input text field
spotify_playlist_url = st.text_input("", placeholder="https://open.spotify.com/playlist/YOUR_PLAYLIST_ID", label_visibility="collapsed")
st.divider()

# Extract playlist IDs from URLs
youtube_playlist_id = extract_playlist_id(youtube_playlist_url)
spotify_playlist_id = extract_spotify_playlist_id(spotify_playlist_url)

# submit button
if st.button("submit"):
    
    if youtube_playlist_id and spotify_playlist_id:
        idx = 1
        st.divider()
        st.write("Song Names and Spotify URIs:")
        result = get_song_names_from_link(youtube_playlist_id)
        track_uris = []
        for song_name in result:
            track_uri = search_song(token, song_name)
            if track_uri:
                track_uris.append(track_uri)
                st.write(f"{idx}. {song_name} - {track_uri}")
            else:
                st.write(f"{idx}. {song_name} - Not found on Spotify")
            idx += 1

        if track_uris:
            success = add_songs_to_spotify_playlist(token, spotify_playlist_id, track_uris)
            if success:
                st.success("Songs added to Spotify playlist successfully!")
            else:
                st.error("Failed to add songs to Spotify playlist.")
    else:
        st.warning("Please enter valid YouTube and Spotify Playlist URLs.")

