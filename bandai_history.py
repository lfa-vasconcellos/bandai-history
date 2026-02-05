import sys
import argparse
import os
from api_requests import fetch_data
from dotenv import load_dotenv
from tournament_data import tabulate_results, results_vs_player, tabulate_all_winrates, print_player_results

EVENTS_DIR_PATH="events"

"""
Bearer token to authenticate requests to the bandai-plus-tcg api.
TODO: See if there are public endpoints to check event data OR sign in without having to 
manually fill the token in this script.
"""
BEARER_TOKEN: str = ""
    
if __name__ == "__main__":
    load_dotenv()
    if not os.getenv("BEARER_TOKEN"):
        print('Bearer token not found', file=sys.stderr)
        exit(1)
    BEARER_TOKEN = str(os.getenv("BEARER_TOKEN"))

    if os.getenv("EVENTS_DIR_PATH") is not None:
        EVENTS_DIR_PATH = os.getenv("EVENTS_DIR_PATH") or ""

    # Making sure we have a target directory to place the event files.
    try:
        if not os.path.isdir(EVENTS_DIR_PATH):
            os.mkdir(EVENTS_DIR_PATH)
    except:
        print('Could not create events directory', file=sys.stderr)
        exit(1)

    cli_arg_parser = argparse.ArgumentParser(description="Simple script to compile your results from the bandai plus tcg app.")
    cli_arg_parser.add_argument("-s", "--skip-listing", action="store_true", help="skip request to list events, work with data already requested")
    cli_arg_parser.add_argument("-g", "--group-winrates", action="store_true", help="group your results by opponents bandai id")
    cli_arg_parser.add_argument("-t", "--target", type=str, help="instead of listing results, calculate wins vs losses against a single bandai id")
    
    args = cli_arg_parser.parse_args()

    event_data = fetch_data(BEARER_TOKEN, EVENTS_DIR_PATH, args.skip_listing)
    print("==========")

    if args.group_winrates:
        print_player_results(tabulate_all_winrates(event_data))
    elif args.target is None:
        tabulate_results(event_data)
    else:
        print(results_vs_player(args.target, event_data))
    