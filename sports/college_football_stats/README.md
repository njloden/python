# College Football Player Stats Comparison

This script fetches college football player stats for specified teams and positions using the CollegeFootballData API, and prints them in an easy to compare tabular format.

## Pre-requisites

1. **Install Python:**  
   https://www.python.org/downloads/
2. **Install pip:**  
   https://pip.pypa.io/en/stable/installation/
3. **Install required packages:**  
   `pip install -r requirements.txt`
4. **Generate your API key:**  
   https://collegefootballdata.com/
5. **Set your API key as an environment variable:**  
   `export CFB_API_KEY="your_api_key_here"`


## Usage

Run the script from the command line:


```
python get-cfb-stats.py --position [qb|rb|wr|te|pk|all] --teams "team name1" "team name2"
```

Or, to use a csv file as your player list:

```
python get-cfb-stats.py --position [qb|rb|wr|te|pk|all] --teams "team name1" "team name2" ... [--input-csv "/path/to/player_list.csv"]
```

Or, to use a Google Sheet as your player list:

```
python get-cfb-stats.py --position [qb|rb|wr|te|pk|all] --teams "team name1" ... \
   --input-google-sheet-id "<sheet_id>" \
   --input-google-sheet-range "<sheet_range>" \
   --input-google-sheet-auth-path "/path/to/client_secret.json"
```


### Examples

**Basic Example:**
```
python get-cfb-stats.py --position qb --teams "kansas state" "iowa state"
```


**CSV Example:**
```
python get-cfb-stats.py --position qb --teams "kansas state" "iowa state" --input-csv "/home/deck/Downloads/Fantasy NCAA Player List 2025 - Player List.csv"
```

**Google Sheets Example:**
```
python get-cfb-stats.py --position qb --teams "nebraska" \
   --input-google-sheet-id "1a_LykuvlWocJNK8oMXp7epssmzU_M-YFeb7JOGG4EFQ" \
   --input-google-sheet-range 'Player List!A1:Z1000' \
   --input-google-sheet-auth-path "/home/deck/college-football-api/oauth-secret/google-oauth-client-creds.json"
```


- `--position` specifies the player position to filter (e.g., qb, rb, wr, te, pk, all).
- `--teams` specifies one or more team names (use quotes for names with spaces).
- `--input-csv` (optional) specifies a CSV file containing player names. If provided, only players listed in the CSV will be included in the output. The CSV should have player names in the format: `POSITION,First,Last,...` (e.g., `QB,Trey,Owens,...`).
- `--input-google-sheet-id` (optional) specifies the Google Sheet ID to use as a player list. Only players listed in the sheet will be included in the output.
- `--input-google-sheet-range` (optional) specifies the A1 range in the Google Sheet (e.g., `'Player List!A1:Z1000'`).
- `--input-google-sheet-auth-path` (optional) specifies the path to your Google OAuth2 client_secret.json file for authentication.

### Google Sheets Notes

- The Google Sheet should have player data in the format: `POSITION,First,Last,...` (e.g., `QB,Trey,Owens,...`).
- You must use a Google OAuth2 client credentials file (`client_secret.json`) and authenticate on first use.
- The script will prompt you to log in to your Google account if needed.

#### Setting up Google OAuth Client Secrets

To use Google Sheets as input, you need to create OAuth2 credentials for a Desktop app:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Create or select a project.
3. Click **Create Credentials** > **OAuth client ID**.
4. Choose **Desktop app** as the application type.
5. Download the `client_secret.json` file and save it to your project directory (e.g., `/home/deck/college-football-api/oauth-secret/google-oauth-client-creds.json`).
6. On first run, the script will prompt you to log in and authorize access to your Google Sheets.

For more details, see the [Google documentation on OAuth client IDs](https://developers.google.com/workspace/guides/create-credentials#oauth-client-id).


## Notes

- The script fetches all players for the listed teams, then filters by position.
- Some players may be missing if not on those teams.
- Stats are grouped by category to avoid overwriting (e.g., passing, rushing, receiving).
- Some players may have multiple categories of stats.
- Stats are displayed with players as columns and stats as rows, which may be easier to read when comparing multiple players.


## Output

- The script prints a table of player stats for the specified position and teams.
- If no players are found for the given position, a message is displayed.

### Example

Below is a sample output for the command:

```
python get-cfb-stats.py --position qb --teams "kansas state" "iowa state"
```

```
Position: qb

╒═════════════════════╤═════════════════╤═══════════════╕
│                     │ Avery Johnson   │ Rocco Becht   │
╞═════════════════════╪═════════════════╪═══════════════╡
│ Team                │ Kansas State    │ Iowa State    │
├─────────────────────┼─────────────────┼───────────────┤
│ passing_ATT         │ 30              │ 28            │
├─────────────────────┼─────────────────┼───────────────┤
│ passing_COMPLETIONS │ 21              │ 14            │
├─────────────────────┼─────────────────┼───────────────┤
│ passing_INT         │ 0               │ 0             │
├─────────────────────┼─────────────────┼───────────────┤
│ passing_PCT         │ 0.700           │ 0.500         │
├─────────────────────┼─────────────────┼───────────────┤
│ passing_TD          │ 2               │ 2             │
├─────────────────────┼─────────────────┼───────────────┤
│ passing_YDS         │ 273             │ 183           │
├─────────────────────┼─────────────────┼───────────────┤
│ passing_YPA         │ 9.1             │ 6.5           │
├─────────────────────┼─────────────────┼───────────────┤
│ rushing_CAR         │ 8               │ 12            │
├─────────────────────┼─────────────────┼───────────────┤
│ rushing_LONG        │ 10              │ 9             │
├─────────────────────┼─────────────────┼───────────────┤
│ rushing_TD          │ 1               │ 1             │
├─────────────────────┼─────────────────┼───────────────┤
│ rushing_YDS         │ 21              │ 18            │
├─────────────────────┼─────────────────┼───────────────┤
│ rushing_YPC         │ 2.6             │ 1.5           │
├─────────────────────┼─────────────────┼───────────────┤
│ fumbles_FUM         │                 │ 1             │
├─────────────────────┼─────────────────┼───────────────┤
│ fumbles_LOST        │                 │ 1             │
├─────────────────────┼─────────────────┼───────────────┤
│ fumbles_REC         │                 │ 0             │
╘═════════════════════╧═════════════════╧═══════════════╛
```

## Requirements

See `requirements.txt` for the list of required Python packages.

## License

This script is provided as-is for educational and personal use. See the CollegeFootballData API terms of service for API usage restrictions.
