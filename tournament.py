#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament


# imports the db.py helper module to handle database connection,
# querying, executing and closing
from DB import *


# deletes all the entries in matches table
def deleteMatches():
    """Remove all the match records from the database."""
    q = "TRUNCATE matches;"
    DB().execute(q, False, True)


# deletes all the entries in players table
def deletePlayers():
    """Remove all the player records from the database."""
    q = "TRUNCATE players CASCADE;"
    DB().execute(q, False, True)


# returns the number of registered players
def countPlayers():
    """Returns the number of players currently registered."""
    q = "SELECT count(*) FROM players"
    t = DB().execute(q, False)
    r = t["cursor"].fetchone()
    t["conn"].close()
    return r[0]


# adds player to players table
def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    q = "INSERT INTO players (name) VALUES (%s)"
    p = (name,)
    DB().execute(q, p, True)


# returns a list of tuples with id, name, wins and matches of a players
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    q = """
        SELECT players.id, players.name, coalesce(wintable.wins, 0),
        coalesce(matchtable.matches, 0)
        FROM players
        LEFT JOIN wintable ON players.id = wintable.id
        LEFT JOIN matchtable ON players.id = matchtable.id
        ORDER BY CASE WHEN wins is null THEN 1 ELSE 0 END, wins desc;
        """
    t = DB().execute(q, False)
    r = ([(row[0], row[1], int(row[2]), int(row[3]))
         for row in t["cursor"]
         .fetchall()])
    t["conn"].close()
    return r


# records a match between two players and posibble tied outcome
def reportMatch(player1, player2, tied=False):
    """Records the outcome of a single match between two players.
    Args:
      player1: the id number of the player who won
      player2: the id number of the player who lost
      tied: in case outcome of game is tied game,
      third paramter outcome paramter should be passed as true (1) or false (0)
    """
    if tied:
        q = "INSERT INTO matches (player1,player2,tied) VALUES (%s, %s, %s)"
        p = (player1, player2, tied)
    else:
        q = "INSERT INTO matches (player1,player2) VALUES (%s, %s )"
        p = (player1, player2)
    DB().execute(q, p, True)


# returns a list of pairs of players for the next round of a match
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
    for p1, p2 in zip(ps[0::2], ps[1::2]):
        r.append((p1[0], p1[1], p2[0], p2[1]))

    return r
