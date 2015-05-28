#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) from players;")
    r = c.fetchone()
    DB.close()
    return r[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)",(name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    q = """
        SELECT players.id, players.name, coalesce(wintable.wins, 0), coalesce(matchtable.matches, 0)
        FROM players
        LEFT JOIN (
            SELECT winner as id, count(winner) as wins
            FROM matches
            GROUP BY winner) AS wintable ON players.id = wintable.id
        LEFT JOIN (
            SELECT id, count(id) as matches
            FROM players, matches
            WHERE players.id = winner OR players.id = loser
            GROUP BY id) AS matchtable ON players.id = matchtable.id
        ORDER BY CASE WHEN wins is null THEN 1 ELSE 0 END, wins desc;
        """
    c.execute(q)
    r = [(row[0], row[1], int(row[2]), int(row[3])) for row in c.fetchall()]
    DB.close()
    return r


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (winner,loser) values (%s, %s)",(winner,loser))
    DB.commit()
    DB.close()


def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
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
    ps = playerStandings()
    r = []

    # http://discussions.udacity.com/t/idiomatic-code-for-swisspairings-function/17210
    for p1, p2 in zip(ps[0::2],ps[1::2]):
        r.append((p1[0], p1[1], p2[0], p2[1]))

    return r
