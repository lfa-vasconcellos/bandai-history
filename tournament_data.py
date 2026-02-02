from collections import defaultdict

"""
Returns (wins, losses) for the tournament
"""
def tabulate_single_event(event_data):
    wins = 0
    losses = 0
    
    rounds = event_data['rounds']
    for round in rounds:
        if round['is_win']:
            wins += 1
        else:
            losses += 1

    return (wins, losses)


"""
Count every possible result in the player's history (e.g: player had 3 3-1s, etc.)
"""
def tabulate_results(events_data):
    player_results = defaultdict(int)
    player_results_by_losses = defaultdict(int)

    for event in events_data:
        result = tabulate_single_event(event)
        player_results[result] += 1
    sorted_results = dict(sorted(player_results.items(), key=lambda x: x[0][1]))

    for result, qty in sorted_results.items():
        # Skipping tournaments that stores asked us to apply just for the record
        if result[0] == 0 and result[1] == 0: continue

        print(f"{result[0]}-{result[1]}: {qty}")
        player_results_by_losses[result[1]] += qty

    print("=============================")
    for result, qty in player_results_by_losses.items():
        print(f"X-{result}: {qty}")


def tabulate_all_winrates(events_data):
    players_results = dict()

    for event in events_data:
        for round in event['rounds']:
            if 'membership_number' not in round['opponent_users'][0]:
                continue
            else:
                user_bandai_id = round['opponent_users'][0]['membership_number']
                if user_bandai_id not in players_results:
                    if round['is_win']:
                        players_results[user_bandai_id] = [1, 0]
                    else:
                        players_results[user_bandai_id] = [0, 1]
                else:
                    if round['is_win']:
                        players_results[user_bandai_id][0] += 1
                    else:
                        players_results[user_bandai_id][1] += 1

    return players_results


def load_bandai_username_id():
    username_map = dict()

    with open("bandai_username_map.txt") as f:
        for line in f:
            username, banda_id = line.strip().split(":")
            username_map[banda_id] = username

    return username_map

"""
To be used with the result of `tabulate_all_winrates`
"""
def print_player_results(player_results):
    username_map = load_bandai_username_id()
    
    sorted_results = dict(sorted(player_results.items(), key=lambda x: x[1][0], reverse=True))
    for player_id, res in sorted_results.items():
        tag = player_id
        if player_id in username_map:
            tag = username_map[player_id]
        print(f"{tag}: {res[0]}-{res[1]}")

"""
Count results against single player
"""
def results_vs_player(player_bandai_id, events_data):
    wins, losses = (0, 0)

    for event in events_data:
        for round in event['rounds']:
            if 'membership_number' not in round['opponent_users'][0] or round['opponent_users'][0]['membership_number'] != player_bandai_id:
                continue
            if round['is_win']:
                wins += 1
            else:
                losses += 1

    return (wins, losses)