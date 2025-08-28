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
python get-cfb-stats.py --position [qb|rb|wr|te|pk|all] --teams "team name1" "team name2" ...
```

### Example

```
python get-cfb-stats.py --position qb --teams "kansas state" "iowa state"
```

- `--position` specifies the player position to filter (e.g., qb, rb, wr, te, pk, all).
- `--teams` specifies one or more team names (use quotes for names with spaces).

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
