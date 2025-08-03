from instagrapi import Client

USERNAME = "ajinkyaghuge42"
PASSWORD = "ajinkyaghuge@2020"

cl = Client()

try:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("settings.json")
    print(" Login successful and session saved.")
except Exception as e:
    print(f" Failed to login and save session: {e}")
