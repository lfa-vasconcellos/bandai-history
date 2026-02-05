# Bandai TCG Results List

This is a simple script to compile all your results from the Bandai TCG Plus app. This is a WIP.

## Disclaimer

Even though this script makes only one request per second and uses good practices, this is an *unauthorized* used of Bandai's API. Use it at your own risk, I'm not responsible if you get your bandai account banned.


## How to use

1. Clone this repo.

2. Install your dependencies (TODO: add dependencies)

```
pip install -r requirements.txt
```

3. Duplicate the `.env.example` file and name it `.env`. Add your bearer token from the app. (You can check it in your `network` tab while using the app in your browser)
   <img width="2559" height="1270" alt="image" src="https://github.com/user-attachments/assets/57e352f0-7725-4333-bc7a-fc4482b9c954" />


5. Run the script

```
python3 bandai_history.py
```


### Options

- Since this script saves every tournament as a json file under `events`, you can pass the `-s` flag after the first time to skip the events listing.

- You can pass a target with the flag `-t` to count only the results agains a single player:

```
python3 bandai_history.py -t XXXXXXXX
```

- You can pass the `-g` flag to group your results by opponents bandai id as well:

```
python3 bandai_history.py -g 
```

Optionally, you can add a file with the name "bandai_username_map.txt" to map your friend's bandai user id to their name. The file should have their names and ids in the following format:
```
FOO:XXXXXXXX
BAR:YYYYYYYY
BAZ:ZZZZZZZZ
```

- You can add a line with 'EVENTS_DIR_PATH' to save your events in a different folder (if you're running this script for a friend, for example)

## Notes, Known Issues, TODOS:

- This script does not compute events with 0 rounds. This may cause a discrepancy in the total number of events and the sum of the results

- This script does not consider each game on your app individually

