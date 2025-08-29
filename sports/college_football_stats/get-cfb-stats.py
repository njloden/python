###
# standard form:
#   python get-cfb-stats.py --position [qb|rb|wr|te|pk|all] --teams "team name1" "team name2" ... \
#     [--input-csv "/path/to/player_list.csv"] \
#     [-input-google-sheet-id "sheet id" --input-google-sheet-range "sheet_range" --input-google-sheet-auth-path "/path/to/client_secret.json"]
# examples:
#   python get-cfb-stats.py --position wr --teams "purdue" "indiana"
#   python get-cfb-stats.py --position qb --teams "kansas state" "iowa state" --input-csv "/path/to/player_list.csv"
#   python get-cfb-stats.py --position rb --teams "alabama" "notre dame" \
#      --input-google-sheet-id "<sheet_id>" \
#      --input-google-sheet-range "<sheet_range>" \
#      --input-google-sheet-auth-path "/path/to/client_secret.json"
# If --input-csv or -input-google-sheet* are provided, only players listed in the input sources will be included in the output.
###
import os
import sys
import csv
import argparse
import requests
import pandas
import collections
import tabulate
import gspread
import oauth2client


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
    parser.add_argument('--input-csv', required=False, help='Input CSV file path with player names')
    parser.add_argument('--input-google-sheet-id', required=False, help='Input google sheet id with player names')
    parser.add_argument('--input-google-sheet-range', required=False, help='Input google sheet range with player names')
    parser.add_argument('--input-google-sheet-auth-path', required=False, help='Input google sheet oauth client secret path')
    return parser.parse_args()


def extract_full_names_from_csv(csv_path):
    """
    Reads a CSV file and returns a list of all player full names (first + last) found in the file.
    Only lines with player data are processed.
    Example CSV:
    WR,,,,WR,,,,WR,Malik,McClain,,WR,Romello,Brinson
    """
    positions = {"QB", "WR", "RB", "TE", "K", "DEF"}
    names = set()
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            i = 0
            while i < len(row) - 2:
                pos = row[i]
                first = row[i+1]
                last = row[i+2]
                if (
                    isinstance(pos, str) and pos.strip() in positions and
                    isinstance(first, str) and first.strip() and
                    isinstance(last, str) and last.strip()
                ):
                    full_name = f"{first.strip()} {last.strip()}".lower()
                    names.add(full_name)
                    i += 3
                else:
                    i += 1
    return names


def get_sheet_values(sheet_id, range_name, client_secret_path, token_path='token.json'):
    """
    Fetches values from a private Google Sheet using OAuth2 user credentials (Installed App flow).
    Args:
        sheet_id (str): The Google Sheet ID.
        range_name (str): The A1 notation range (e.g., 'Sheet1!A1:E100').
        client_secret_path (str): Path to the OAuth2 client_secret.json file.
        token_path (str): Path to store the user's access/refresh token.
    Returns:
        list: List of rows (each row is a list of cell values as strings).
    """
    import os
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    store = oauth2client.file.Storage(token_path)
    creds = store.get()
    if not creds or creds.invalid:
        flow = oauth2client.client.flow_from_clientsecrets(client_secret_path, scope)
        creds = oauth2client.tools.run_flow(flow, store)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(range_name.split('!')[0])
    return worksheet.get_all_values()


def extract_full_names_from_sheets(rows):
    """
    Given a list of rows (each a list of strings), extract first and last names
    (assuming the pattern: [position, first, last, ...]), combine them, and return a list of full names.
    """
    full_names = []
    for row in rows:
        i = 0
        while i < len(row) - 2:
            pos, first, last = row[i], row[i+1], row[i+2]
            if pos and first and last:
                full_names.append(f"{first} {last}")
                i += 3
            else:
                i += 1
    return full_names


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
        "stats": collections.defaultdict(dict)
    }


def get_team_stats(team_name, available_players=None):
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
    players = collections.defaultdict(create_player_dict)

    # Iterate over each stat record in the API response
    for record in data:
        player_name = record["player"]
        # Only add player if not filtering, or if player is in available_players (case-insensitive)
        if available_players is not None and player_name.lower() not in available_players:
            continue
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


def build_comparison_table(players_list, position, available_players=None):
    """
    Build and print a comparison table of player stats for a given position.
    Args:
        players_list (list): List of player dictionaries.
        position (str): Player position to filter and display.
    Returns:
        None
    """
    rows = []
    pos_key = position.upper() if position.lower() != 'all' else None

    for player in players_list:
        player_pos = player["position"].upper()
        # Only filter by position now
        if position.lower() == "all" or player_pos == pos_key:
            flat_stats = {
                "Player": f"{player['player']}",
                "Team": f"{player['team']}"
            }
            for category, stats in player["stats"].items():
                for stat_name, stat_val in stats.items():
                    col_name = f"{category}_{stat_name}"
                    flat_stats[col_name] = stat_val
            rows.append(flat_stats)

    # If no players matched the position, print a message and exit the function
    if not rows:
        print(f"No players found for position: {position}")
        return

    # Create a DataFrame from the rows and fill missing values with empty strings
    df = pandas.DataFrame(rows).fillna("")
    # Transpose the DataFrame so stats are rows and players are columns
    df = df.set_index("Player").T  # transpose: stats as rows, players as columns

    # Print the position and the formatted table
    print(f"\nPosition: {position}\n")
    print(tabulate.tabulate(df, headers="keys", tablefmt="fancy_grid"))


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
    input_csv_path = args.input_csv
    input_google_sheet_id = args.input_google_sheet_id
    input_google_sheet_range = args.input_google_sheet_range
    input_google_sheet_client_auth_path = args.input_google_sheet_auth_path
    # if google sheet args are provided, ensure all are present
    if (input_google_sheet_id or input_google_sheet_range or input_google_sheet_client_auth_path) and not (input_google_sheet_id and input_google_sheet_range and input_google_sheet_client_auth_path):
        print("Error: If using Google Sheet input, please provide --input-google-sheet-id, --input-google-sheet-range, and --input-google-sheet-auth-path.")
        sys.exit(1)    

    # if provided as an arg, check file and extract all available players from CSV
    if input_csv_path is not None:
        if not os.path.isfile(input_csv_path) or not os.access(input_csv_path, os.R_OK):
            print(f"Error: The file '{input_csv_path}' does not exist or is not readable.")
            sys.exit(1)
        available_players = extract_full_names_from_csv(input_csv_path)
    # if provided as an arg, check google sheet and extract all available players
    elif input_google_sheet_id is not None:
        available_players = extract_full_names_from_sheets(get_sheet_values(input_google_sheet_id, input_google_sheet_range, input_google_sheet_client_auth_path))
    else:
        available_players = None

    # Loop through each team, fetch player stats, and add them to the list
    all_players = []
    for team in team_list:
        all_players.extend(get_team_stats(format_team_name(team), available_players=available_players))

    # Build and print the comparison table for the specified position
    build_comparison_table(all_players, position, available_players=available_players)


if __name__ == "__main__":
    main()
