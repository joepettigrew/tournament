#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM matches;"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM players;"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = "SELECT COUNT(*) FROM players;"
    c.execute(query)
    rows = c.fetchone()
    return int(rows[0])
    db.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # Sanitize input
    bleach.clean(name)

    # Execute query
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (player_name) VALUES (%s)", (name, ))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # Execute query
    db = connect()
    c = db.cursor()
    query = """
    SELECT
        p.player_id,
        p.player_name,
        COUNT(CASE WHEN m.winner THEN 1 END) as wins,
        COUNT(m.player_id) as matches
    FROM players as p
    LEFT JOIN matches as m
    ON p.player_id = m.player_id
    GROUP BY p.player_id
    ORDER BY wins DESC;
    """
    c.execute(query)
    return c.fetchall()
    db.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Sanitize the input
    bleach.clean(winner)
    bleach.clean(loser)

    # Connect to DB
    db = connect()
    c = db.cursor()

    # Record the winner
    c.execute("""
    INSERT INTO matches (winner, player_id)
    VALUES (True, %s);
    """, (winner,))
    db.commit()

    # Record the loser
    c.execute("""
    INSERT INTO matches (winner, player_id)
    VALUES (False, %s);
    """, (loser,))
    db.commit()

    # Close DB connection
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Get the playerStandings results
    rows = playerStandings()

    # Create new tuples of pairings
    pairing = []
    for i in xrange(0, len(rows), 2):
        pairing.append((rows[i][0], rows[i][1], rows[i+1][0], rows[i+1][1]))
    return pairing
