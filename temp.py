

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
#     # print(json_result)

#     token = json_result["access_token"]
#     return token

# def get_auth_header(token):
#     return {"Authorization": "Bearer " + token}

# def search_for_artist_id(token, artist_name):
#     search_url = "https://api.spotify.com/v1/search"
#     headers = get_auth_header(token)
#     search_query = f"?q={artist_name}&type=artist&limit=1"

#     actual_search_query= search_url + search_query

#     result = get(actual_search_query, headers=headers)
#     json_result = json.loads(result.content)["artists"]["items"]

#     if len(json_result)==0:
#         print("No Artist Exist")
#         return None
    
#     artist_id = json_result[0]["id"]

#     return artist_id



    

# token = get_token()

# artist_id = search_for_artist_id(token,"Thaman S")

# songs = get_songs_by_artists(token,artist_id)

# print("token:" + token)
# print("Artits: ",artist_id)

# for idx,songs in enumerate(songs):
#     print(f"{idx+1}. {songs['name']}")



