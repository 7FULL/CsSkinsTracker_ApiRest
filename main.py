import json
import flask
from flask import request
import requests
from flask_cors import CORS
from utils import load_skins_tracker, load_history

app = flask.Flask(__name__)
cors = CORS()
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})


@app.route('/api/add-skin', methods=["POST"])
def add_skin_to_tracker():
    skin_name = request.json["skin_name"]
    hash_name = request.json["hash_name"]

    skins_tracker = load_skins_tracker()

    # We check if the skin is already in the tracker
    for skin in skins_tracker:
        if skin["hash_name"] == hash_name:
            return "Skin already in the tracker", 400

    # We add to the json file and the list
    skin = {
        "name": skin_name,
        "hash_name": hash_name
    }

    skins_tracker.append(skin)

    try:
        with open("skins_tracker.json", "w") as file:
            skins_tracker_json = {
                "skins": skins_tracker
            }

            json.dump(skins_tracker_json, file, indent=4)
    except Exception as e:
        return f"Error adding the skin to the tracker: {str(e)}", 500

    return "Skin added to the tracker", 201


@app.route('/api/update-skin', methods=["PUT"])
def update_skin_in_tracker():
    name = request.json["name"]
    hash_name = request.json["hash_name"]

    skins_tracker = load_skins_tracker()

    # We check if the skin is in the tracker
    for skin in skins_tracker:
        if skin["name"] == name:
            skin["hash_name"] = hash_name

            try:
                with open("skins_tracker.json", "w") as file:
                    skins_tracker_json = {
                        "skins": skins_tracker
                    }

                    json.dump(skins_tracker_json, file, indent=4)
            except Exception as e:
                return f"Error updating the skin in the tracker: {str(e)}", 500

            return "Skin updated in the tracker", 200

    return "Skin not found in the tracker", 404


@app.route('/api/remove-skin', methods=["DELETE"])
def remove_skin_from_tracker():
    name = request.json["name"]

    skins_tracker = load_skins_tracker()

    # We check if the skin is in the tracker
    for skin in skins_tracker:
        if skin["name"] == name:
            skins_tracker.remove(skin)

            try:
                with open("skins_tracker.json", "w") as file:
                    skins_tracker_json = {
                        "skins": skins_tracker
                    }

                    json.dump(skins_tracker_json, file, indent=4)
            except Exception as e:
                return f"Error removing the skin from the tracker: {str(e)}", 500

            return "Skin removed from the tracker", 200

    return "Skin not found in the tracker", 404


@app.route('/api/skins-tracker')
def get_skins_tracker():
    skins_tracker = load_skins_tracker()

    return json.dumps(skins_tracker)


@app.route('/api/skins-history')
def get_skins_history():
    history = load_history()

    return json.dumps(history)


if __name__ == "__main__":
    app.run(debug=True)


