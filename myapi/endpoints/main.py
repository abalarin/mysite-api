from flask import Blueprint, jsonify
from flask_cors import CORS
from .utils import get_albums, get_images, spotify_feed, github_feed

main = Blueprint("main", __name__)

CORS(main) # enable CORS on the main blue print

@main.route("/", methods=["GET"])
def index():
    return {"Success": "You've hit the api"}

@main.route("/albums", methods=["GET"])
def albums():
    try:
        results = get_albums()

        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})

@main.route('/images/<album>', methods=['GET'])
def pictures(album):
    try:
        results = get_images(album)

        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})

@main.route('/music/<count>')
def music(count):
    return spotify_feed(count)

@main.route('/github/<count>')
def githubjson(count):
    return jsonify(github_feed(count))

@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return {"error": "resource not found"}
