import json
import requests

from flask import jsonify

from myapi.app import session, client, config
from myapi.models.site_models import Configuration

def get_albums():
    try:
        result = client.list_objects(Bucket='austin', Prefix='albums/', Delimiter='/')
        album_names = []
        for object in result.get('CommonPrefixes'):
            album_names.append(object['Prefix'][6:].strip('/'))

        albums = []
        for album_name in album_names:
            album = {
                'Name': album_name,
                'images': get_images(album_name)
            }
            albums.append(album)

        return albums

    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})

def get_URL(file_name):
    return client.generate_presigned_post(Bucket='austin', Key=file_name)

def get_images(album):
    try:
        prefix = 'albums/' + str(album) + '/'
        result = client.list_objects(Bucket='austin', Prefix=prefix, Delimiter='/')

        image_urls = []
        skipthedir = 0  # becuase the directory itself is also retrived we want to skip it
        for object in result.get('Contents'):
            if skipthedir > 0:
                url = get_URL(object.get('Key'))
                image_urls.append(url.get('url') + '/' + url.get('fields')['key'])
            else:
                skipthedir += 1

        return image_urls


    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})

def authenticate_spotify():
    """ Gets new spotify bearer token """

    configuration = session.query(Configuration).filter_by(id=1).first()

    # Build out spotify authentication POST
    grant_type = "grant_type=authorization_code"
    code = "&code=" + configuration.spotify_code
    redirect_uri = "&redirect_uri=" + config.SPOTIFY_REDIRECT
    client_id = "&client_id=" + config.SPOTIFY_ID
    client_secret = "&client_secret=" + config.SPOTIFY_SECRET

    payload = grant_type + code + redirect_uri + client_id + client_secret

    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = 'https://accounts.spotify.com/api/token'

    # Once authenticated, Bearer Token will be returned for User data access
    response = requests.post(url, data=payload, headers=headers)
    access_token = json.loads(response.text)['access_token']
    refresh_token = json.loads(response.text)['refresh_token']

    # Update Site Configuration Table with Spotify Bearer Token
    config.spotify_access_token = access_token
    config.spotify_refresh_token = refresh_token
    db.session.commit()


def reauth_spotify():
    """ Get a new  Spotify access token with the Refresh token """

    configuration = session.query(Configuration).filter_by(id=1).first()
    print(config)

    # Build out spotify authentication POST
    grant_type = "grant_type=refresh_token"
    refresh_token = "&refresh_token=" + configuration.spotify_refresh_token
    client_id = "&client_id=" + config['SPOTIFY_ID']
    client_secret = "&client_secret=" + config['SPOTIFY_SECRET']

    payload = grant_type + refresh_token + client_id + client_secret

    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = 'https://accounts.spotify.com/api/token'

    # Once authenticated, Bearer Token will be returned for User data access
    response = requests.post(url, data=payload, headers=headers)
    access_token = json.loads(response.text)['access_token']

    # Update Site Configuration Table with Spotify Bearer Token
    configuration.spotify_access_token = access_token
    
    session.add(configuration)
    session.commit()

    return access_token


def spotify_feed(limit):
    """ Return # of the most recent Spotify Songs Played """

    url = "https://api.spotify.com/v1/me/player/recently-played"
    querystring = {"limit": str(limit)}
    # token =session.query(Configuration).first().spotify_access_token)
    headers = {
        'Authorization': "Bearer " + session.query(Configuration).first().spotify_access_token
    }

    response = requests.get(url, data="", headers=headers, params=querystring)
    response = json.loads(response.text)

    # Check if the Access Token is not expired, if not KeyError will be thrown
    try:
        if response['error']:
            headers = {
                'Authorization': "Bearer " + reauth_spotify()
            }

            response = requests.get(
                url, data="", headers=headers, params=querystring)
            response = json.loads(response.text)
            return response

    # If Key Error is thrown then there was no error in get request, return original response
    except KeyError:
        return response

    return response
