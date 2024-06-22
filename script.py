import json
import random
import time

import requests


def get_skin_info(skin_name):
    url = f"https://steamcommunity.com/market/priceoverview/?country=DE&currency=3&appid=730&market_hash_name={skin_name}"
    response = requests.get(url)
    data = response.json()

    if data["success"]:
        return data
    else:
        raise Exception("Error getting the skin info")


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


def update_history(hour, date):
    skins_tracker = load_skins_tracker()
    history = load_history()

    for skin in skins_tracker:
        skin_info = get_skin_info(skin["hash_name"])
        price = skin_info["median_price"]
        lowest_price = skin_info["lowest_price"]
        volume = skin_info["volume"]

        if price and history is not None:
            # If the skin is not in the history we add it
            if skin["name"] not in history:
                history[skin["name"]] = []

            item = {
                "price": price,
                "lowest_price": lowest_price,
                "volume": volume,
                "hour": hour,
                "date": date
            }

            history[skin["name"]].append(item)

        # We wait a random time between 1 and 3 seconds
        time.sleep(random.uniform(1, 3))

    history_json = {
        "history": history
    }

    with open("history.json", "w") as file:
        json.dump(history_json, file, indent=4)


minute = time.strftime("%M")

# We wait until is the first beginning of an hour to start the cycle
while minute != "00":
    minute = time.strftime("%M")
    print(f"Waiting for the next hour")

    minutes_left = 60 - int(minute)
    print(f"Minutes left: {minutes_left}")

    time.sleep(20)

# Every hour we update the history
while True:
    hour = time.strftime("%H")
    date = time.strftime("%d/%m/%Y")

    update_history(hour, date)

    time.sleep(3600)
