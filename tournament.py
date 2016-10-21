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
    conn = connect()
    cs = conn.cursor()
    cs.execute("Delete from matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cs = conn.cursor()
    cs.execute("Delete from players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cs = conn.cursor()
    cs.execute("select count(*) from players;")
    res = cs.fetchone()
    conn.commit()
    conn.close()
    print res
    return int(res[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cs = conn.cursor()
    cs.execute("insert into players(name) values(%s)", (name,))
    print name
    conn.commit()
    conn.close()


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
    conn = connect()
    cs = conn.cursor()
    cs.execute(
        "select players.pid, players.name, (select count(matches.mid) from matches\
        where players.pid = matches.winner) as wins, \
        (select count(matches.mid) from matches where players.pid = \
        matches.winner or players.pid = matches.loser) as total from players \
        order by wins DESC")
    res = cs.fetchall()
    print res
    conn.commit()
    conn.close()
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cs = conn.cursor()
    cs.execute(
        "insert into matches(winner, loser) values(%s,%s)", (winner, loser,))
    conn.commit()
    conn.close()


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
    conn = connect()
    cs = conn.cursor()
    cs.execute(
        "select players.pid, players.name, (select count(matches.mid) \
        from matches where players.pid = matches.winner) as wins, \
        (select count(matches.mid) from matches where players.pid = matches.winner \
        or players.pid = matches.loser) as total from players \
        order by wins DESC")
    res = cs.fetchall()
    conn.commit()
    conn.close()
    pair = []
    i = 0
    while len(res) > 0:
        pair.append((res[0][0], res[0][1]))
        res.pop(0)
        pair[i] += (res[0][0], res[0][1])
        res.pop(0)
        i += 1
    return pair
