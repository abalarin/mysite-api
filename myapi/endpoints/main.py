from flask import Blueprint, jsonify
from flask_cors import CORS
from .utils import get_albums, get_images

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

@main.route('/<album>/images', methods=['GET'])
def pictures(album):
    try:
        return jsonify(get_images(album))
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})

@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return {"error": "resource not found"}
