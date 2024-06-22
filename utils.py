import json


def load_skins_tracker():
    skins_tracker = []

    with open("skins_tracker.json", "r") as file:
        data = json.load(file)
        skins_tracker = data["skins"]

    return skins_tracker


def load_history():
    h = None

    with open("history.json", "r") as file:
        data = json.load(file)
        h = data["history"]

    return h