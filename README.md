TOURNAMENT
===========
A simple tournament app that tracks new players, match results, and creates new pairings based on **Swiss-system**.

REQUIREMENTS
-------------
* Python 2.7
* PostgreSQL

FILE STRUCTURE
-------------
* tournament.py
* tournament_test.py
* tournament.sql

INSTALLATION
-------------
1. Install PostgreSQL on your server
2. Use the included ``tournaments.sql`` to populate the necessary database and tables.
3. Then use the following command lines to execute:

```
$ psql -f tournament.sql
$ python tournament_test.py
```

Once complete, use the following functions to interact with the database:
* ``registerPlayer(name)`` : Register new player
* ``countPlayers()`` : Counts registered players
* ``reportMatch(winner, loser)`` : Record the winner and the loser of a match using their player_id
* ``playerStandings()`` : See the current standings
* ``swissPairings()`` : Generate the next round of a match

You can reset the database for a new tournament by using the following functions:
* ``deleteMatches()`` : Remove all match records
* ``deletePlayers()`` : Remove all players

LICENSE
-------------
The contents of this repository are covered under the [MIT License](LICENSE.md).
