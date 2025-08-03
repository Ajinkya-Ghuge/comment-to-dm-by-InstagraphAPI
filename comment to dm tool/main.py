import json
import os
from instagrapi import Client

USERNAME = "ajinkyaghu42"
PASSWORD = "ajinkyaghuge@202"
REEL_URL = "https://www.instagram.com/reel/DMlRwcECFyu/"
DEFAULT_MESSAGE = "Hey! Thanks for commenting on my reel. Here's something cool for you."
REPLY_MESSAGE = "Thanks for your support!"
MESSAGED_USERS_FILE = "messaged_users.json"

def load_messaged_users():
    if os.path.exists(MESSAGED_USERS_FILE):
        with open(MESSAGED_USERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_messaged_users(messaged_users):
    with open(MESSAGED_USERS_FILE, "w") as f:
        json.dump(list(messaged_users), f)

def run_dm_automation(username, password, reel_url, message, reply_message):
    client = Client()

    try:
        client.load_settings("settings.json")
        client.login(username, password)
        print(" Logged in using saved session.")
    except Exception as e:
        print(f" Login failed: {e}")
        return

    try:
        media_id = client.media_pk_from_url(reel_url)
        comments = client.media_comments(media_id)
        print(f" Fetched {len(comments)} comments.")
    except Exception as e:
        print(f" Failed to fetch comments: {e}")
        return

    messaged_users = load_messaged_users()
    new_messaged_users = set()
    dm_count = 0
    like_count = 0
    reply_count = 0

    for comment in comments:
        user = comment.user

        if user.username in messaged_users:
            continue

        # Send DM
        try:
            client.direct_send(message, [user.pk])
            print(f" DM sent to: {user.username}")
            dm_count += 1
            new_messaged_users.add(user.username)
        except Exception as e:
            print(f" Failed to message {user.username}: {e}")

        # Skip comment like and reply for now (Instagrapi does not support it)
        # Can add when official method exists

    messaged_users.update(new_messaged_users)
    save_messaged_users(messaged_users)

    print(f"\n Summary:\nDMs sent: {dm_count}\nNew users added to list: {len(new_messaged_users)}")

run_dm_automation(USERNAME, PASSWORD, REEL_URL, DEFAULT_MESSAGE, REPLY_MESSAGE)
