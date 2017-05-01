#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except TypeError:
        print("Couldn't connect to DB")


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    query = "TRUNCATE matches;"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    query = "TRUNCATE players CASCADE;"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
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
    # Execute query
    db, c = connect()
    query = "INSERT INTO players (player_name) VALUES(%s)"
    params = (name, )
    c.execute(query, params)
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
    db, c = connect()
    query = """
    SELECT
        p.player_id,
        p.player_name,
        COUNT(CASE WHEN m.winner_id = p.player_id THEN 1 END) as wins,
        COUNT(CASE WHEN m.winner_id = p.player_id OR
                        m.loser_id = p.player_id THEN 1 END) as matches
    FROM matches as m
    RIGHT JOIN players as p
    ON p.player_id = m.winner_id OR p.player_id = m.loser_id
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
    # Connect to DB
    db, c = connect()
    query = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)"
    params = (winner, loser)

    # Record the winner and loser ids
    c.execute(query, params)
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
