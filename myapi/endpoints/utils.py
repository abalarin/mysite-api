from myapi.app import client

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
