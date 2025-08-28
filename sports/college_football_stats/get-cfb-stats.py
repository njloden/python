###
# standard form:
#   python get-cfb-stats.py --position [qb|rb|wr|te|pk|all] --teams "team name1" "team name2" ...
# example:
#   python get-cfb-stats.py --position qb --teams "kansas state" "iowa state"
###
import os
import sys
import argparse
import requests
import pandas as pd
from collections import defaultdict
from tabulate import tabulate

# extract API key from environment variable
API_KEY = os.environ.get("CFB_API_KEY")
if not API_KEY:
    print("Error: Please set your CFB_API_KEY environment variable.")
    sys.exit(1)


# globals
headers = {"Authorization": f"Bearer {API_KEY}"}
base_url = "https://api.collegefootballdata.com/stats/player/season?year=2025&team="


def parse_args():
    """
    Parse command-line arguments for position and teams.
    Returns:
        argparse.Namespace: Parsed arguments with 'position' and 'teams' attributes.
    """
    parser = argparse.ArgumentParser(description="College Football Player Stats Comparison")
    parser.add_argument('--position', required=True, help='Player position: qb, rb, wr, te, pk, all')
    parser.add_argument('--teams', nargs='+', required=True, help='List of team names (in quotes if spaces)')
    return parser.parse_args()


def create_player_dict():
    """
    Create a default player dictionary structure.
    Returns:
        dict: Player dictionary with default fields and nested stats dict.
    """
    return {
        "season": None,
        "playerId": None,
        "player": None,
        "position": None,
        "team": None,
        "conference": None,
        "stats": defaultdict(dict)
    }


def get_team_stats(team_name):
    """
    Fetch player stats for a given team from the API.
    Args:
        team_name (str): Team name (URL-encoded).
    Returns:
        list: List of player dictionaries with stats.
    """
    try:
        resp = requests.get(f"{base_url}{team_name}", headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for team '{team_name}': {http_err} - {resp.text}")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"Network error occurred for team '{team_name}': {err}")
        sys.exit(1)

    # Parse the JSON response from the API
    data = resp.json()
    # Create a defaultdict to store player data, keyed by playerId
    players = defaultdict(create_player_dict)

    # Iterate over each stat record in the API response
    for record in data:
        pid = record["playerId"]  # Unique player ID
        player = players[pid]  # Get or create the player entry
        # Populate player fields
        player["season"] = record["season"]
        player["playerId"] = record["playerId"]
        player["player"] = record["player"]
        player["position"] = record["position"]
        player["team"] = record["team"]
        player["conference"] = record["conference"]

        # Group stats by category (e.g., passing, rushing, receiving)
        category = record.get("category", "general")
        # Store the stat value under the appropriate category and stat type
        player["stats"][category][record["statType"]] = record["stat"]

    # Return a list of all player dictionaries
    return list(players.values())


def build_comparison_table(players_list, position):
    """
    Build and print a comparison table of player stats for a given position.
    Args:
        players_list (list): List of player dictionaries.
        position (str): Player position to filter and display.
    Returns:
        None
    """
    rows = []
    # Iterate through each player in the list
    for player in players_list:
        # Filter players by the specified position (or include all if 'all' is selected)
        if position.lower() == "all" or player["position"].lower() == position.lower():
            # Create a flat dictionary to hold player stats for the table
            flat_stats = {
                "Player": f"{player['player']}",
                "Team": f"{player['team']}"
            }
            # Flatten the nested stats dictionary into single columns
            for category, stats in player["stats"].items():
                for stat_name, stat_val in stats.items():
                    col_name = f"{category}_{stat_name}"  # e.g., 'passing_YDS'
                    flat_stats[col_name] = stat_val
            # Add the player's stats to the rows list
            rows.append(flat_stats)

    # If no players matched the position, print a message and exit the function
    if not rows:
        print(f"No players found for position: {position}")
        return

    # Create a DataFrame from the rows and fill missing values with empty strings
    df = pd.DataFrame(rows).fillna("")
    # Transpose the DataFrame so stats are rows and players are columns
    df = df.set_index("Player").T  # transpose: stats as rows, players as columns

    # Print the position and the formatted table
    print(f"\nPosition: {position}\n")
    print(tabulate(df, headers="keys", tablefmt="fancy_grid"))


def format_team_name(team):
    """
    Format a team name for use in a URL (replace spaces with %20).
    Args:
        team (str): Team name.
    Returns:
        str: URL-encoded team name.
    """
    return team.replace(" ", "%20")


def main():
    """
    Main entry point: parse arguments, fetch stats, and print comparison table.
    Returns:
        None
    """
    # parse command-line arguments
    args = parse_args()
    position = args.position
    team_list = args.teams

    # Initialize a list to hold all player data from all teams
    all_players = []
    # Loop through each team, fetch player stats, and add them to the list
    for team in team_list:
        all_players.extend(get_team_stats(format_team_name(team)))
    # Build and print the comparison table for the specified position
    build_comparison_table(all_players, position)


if __name__ == "__main__":
    main()
