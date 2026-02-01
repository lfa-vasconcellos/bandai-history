from pathlib import Path
import json
import os
import requests
import time

"""
Check the events folder for event ids
"""
def get_event_ids_local(events_path):
    if not os.path.isdir(events_path):
        raise FileNotFoundError("Events directory does not exist.")
    
    directory_path = Path(events_path)
    event_ids = [event.name for event in directory_path.iterdir()]
    
    return event_ids
        

"""
Fetch all events in the player's history.
TODO: add logic to make paginated requests. For now, 1_000 events should be more than enough.
"""
def fetch_event_ids(bearer_token):
    url = 'https://api.bandai-tcg-plus.com/api/user/my/event?favorite=0&game_title_id=&limit=1000&offset=0&past_event_display_flg=1&selected_tab=3'
    req_headers = {
        'X-Authentication': bearer_token
    }
    
    response = requests.get(url, headers=req_headers)
    print(f"Fetch event ids status Code: {response.status_code}")

    if response.status_code == 200:
        event_data = response.json()['success']['events']
        
        event_ids = []
        for event in event_data:
            event_ids.append(event['id'])

        # print(event_ids)
        return event_ids
    else:
        print("Something went wrong when fetching your event history")

"""
Fetch data from a single event
"""
def fetch_single_event_data(bearer_token, events_path, event_id):
    req_headers = {
        'X-Authentication': bearer_token
    }

    filename = os.path.join(events_path, str(event_id))
    if Path(filename).is_file():
        print(f"Event with ID {event_id} data already exists locally")
        with open(filename, "r") as json_file:
            return json.load(json_file)

    url = f"https://api.bandai-tcg-plus.com/api/user/event/{event_id}/history"
    response = requests.get(url, headers=req_headers)
    time.sleep(1)
    # print(f"Fetching event {event_id} status Code: {response.status_code}")

    if response.status_code == 200:
        response_data = response.json()['success']
    
        with open(filename, "w") as json_file:
            json.dump(response_data, json_file, indent=4)
        return response_data
    else:
        print(f"Something went wrong while fetching data for {event_id}")

"""
Fetch each event from player's history and save them in json files
"""
def fetch_data(bearer_token, events_path, skip_list=False):
    event_ids = []
    if skip_list:
        event_ids = get_event_ids_local(events_path)
    else:
        event_ids = fetch_event_ids(bearer_token) 

    no_events = len(event_ids)

    print(f"You have {no_events} in your history")

    event_data = []
    for idx, event_id in enumerate(event_ids):
        print(f"Fetching event {idx + 1} of {no_events} (ID {event_id})")
        # TODO: handle errors
        event_data.append(fetch_single_event_data(bearer_token, events_path, event_id))

    return event_data