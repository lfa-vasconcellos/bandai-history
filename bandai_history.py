import os
from api_requests import fetch_data
from tournament_data import tabulate_results

EVENTS_DIR_PATH="events"

"""
Bearer token to authenticate requests to the bandai-plus-tcg api.
TODO: See if there are public endpoints to check event data OR sign in without having to 
manually fill the token in this script.
"""
BEARER_TOKEN = ""
    
if __name__ == "__main__":
    # TODO: handle errors
    if not os.path.isdir(EVENTS_DIR_PATH):
        os.mkdir("events")

    event_data = fetch_data(BEARER_TOKEN, EVENTS_DIR_PATH, True)
    print("==========")
    tabulate_results(event_data)

