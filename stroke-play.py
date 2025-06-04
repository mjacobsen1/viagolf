import yaml

def calculate_net_score(hole_score, player_handicap, hole_handicap):
    """
    Calculates the net score for a player on a single hole.

    Args:
        hole_score (int): The player's gross score on the hole.
        player_handicap (int): The player's course handicap.
        hole_handicap (int): The hole's handicap.

    Returns:
        int: The player's net score for the hole.
    """
    # Calculate how many strokes the player gets on this hole.
    strokes_received = 0
    if player_handicap > 0:
        if hole_handicap <= player_handicap:
            strokes_received = 1
        if player_handicap > 18 and hole_handicap <= (player_handicap - 18):
            strokes_received = 2

    net_score = hole_score - strokes_received
    return net_score

def calculate_player_scores(data):
    """
    Calculates the gross and net scores for each player, for each hole, and totals.

    Args:
        data (dict): The data loaded from the YAML file.

    Returns:
       dict: A dictionary where keys are player names and values are dictionaries
             containing:
               'gross_scores': list of gross scores for each hole
               'net_scores': list of net scores for each hole
               'total_gross': total gross score
               'total_net': total net score
               'handicap': int # Player's handicap for the round
    """
    player_scores = {}
    for round_data in data.get('rounds', []):  # Iterate through rounds
        player_handicaps = round_data.get('player_handicaps', {})  # Get player handicaps for the round
        for hole_data in round_data.get('holes', []): # Iterate through holes
            hole_number = hole_data['hole']
            hole_handicap = hole_data['handicap']
            for score_data in hole_data['scores']:
                player_name = score_data['player']
                hole_score = score_data['score']

                if player_name not in player_scores:
                    player_scores[player_name] = {
                        'gross_scores': [],
                        'net_scores': [],
                        'total_gross': 0,
                        'total_net': 0,
                        'handicap': player_handicaps.get(player_name, 0)  # Get handicap, default to 0
                    }

                player_handicap = player_scores[player_name]['handicap']
                net_score = calculate_net_score(hole_score, player_handicap, hole_handicap)

                player_scores[player_name]['gross_scores'].append(hole_score)
                player_scores[player_name]['net_scores'].append(net_score)
                player_scores[player_name]['total_gross'] += hole_score
                player_scores[player_name]['total_net'] += net_score
    return player_scores

def calculate_winner(data):
    """
    Calculates the winner of a stroke play golf game from the given data.

    Args:
        data (dict): A dictionary representing the golf game data.  The expected
            structure is:
            {
                'rounds': [
                    {
                        'player_handicaps': {  # Added player handicaps at the round level
                            'Player A': int,
                            'Player B': int,
                            # ...
                        },
                        'holes': [
                            {
                                'hole': int,
                                'handicap': int,
                                'scores': [
                                    {
                                        'player': str,
                                        'score': int,
                                    },
                                    # ... more player scores for the hole
                                ],
                            },
                            # ... more holes
                        ],
                    },
                   # ... more rounds
                ],
            }
            Example:
            {
                'rounds': [
                    {
                        'player_handicaps': {
                            'Player A': 10,
                            'Player B': 15,
                        },
                        'holes': [
                            {
                                'hole': 1,
                                'handicap': 5,
                                'scores': [
                                    {'player': 'Player A', 'score': 4},
                                    {'player': 'Player B', 'score': 5},
                                ],
                            },
                            {
                                'hole': 2,
                                'handicap': 12,
                                'scores': [
                                    {'player': 'Player A', 'score': 3},
                                    {'player': 'Player B', 'score': 4},
                                ],
                            },
                        ],
                    },
                ],
            }

    Returns:
        tuple: A tuple containing:
            - str: The name of the winner (or "Tie" if there is a tie).
            - dict: A dictionary of all player scores.
    """
    player_scores = calculate_player_scores(data)

    if not player_scores:
        return "No players found.", {}

    # Find the minimum net score.
    min_net_score = float('inf')
    winners = []
    for player, scores in player_scores.items():
        if scores['total_net'] < min_net_score:
            min_net_score = scores['total_net']
            winners = [player]
        elif scores['total_net'] == min_net_score:
            winners.append(player)

    if len(winners) == 1:
        return winners[0], player_scores
    else:
        return "Tie", player_scores

def read_yaml_file(filepath):
    """
    Reads the golf game data from a YAML file.

    Args:
        filepath (str): The path to the YAML file.

    Returns:
        dict: The data read from the YAML file, or None if an error occurs.
    """
    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML format in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading {filepath}: {e}")
        return None

def main():
    """
    Main function to run the golf game calculator.
    """
    filepath = input("Enter the path to the YAML file: ")
    data = read_yaml_file(filepath)
    if data is None:
        return  # Exit if there was an error reading the file

    winner, player_scores = calculate_winner(data)

    if winner: # Check if winner is not None or ""
        print(f"Winner: {winner}")
        print("\nPlayer Scores:")
        for player, scores in player_scores.items():
            print(f"  {player}:")
            print(f"    Handicap: {scores['handicap']}")  # Display handicap
            print(f"    Gross Scores: {scores['gross_scores']}")
            print(f"    Net Scores: {scores['net_scores']}")
            print(f"    Total Gross: {scores['total_gross']}")
            print(f"    Total Net: {scores['total_net']}")
    else:
        print("No winner could be determined.")

if __name__ == "__main__":
    main()

