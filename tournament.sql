-- Table definitions for the tournament project.

-- 1. Start clean and delete tournament database if allready exists
DROP DATABASE tournament;

-- 2. Create database
CREATE DATABASE tournament;

-- 3. Connect to the database
\c tournament

-- 4. Create players Table
CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT
);

-- 5. Create matches Table, tied defines tied (true) or nontied match (false)
CREATE TABLE matches (
  player1 INTEGER REFERENCES players(id),
  player2 INTEGER REFERENCES players(id),
  tied BOOLEAN NOT NULL default false
);

-- 6. Create views: wintable and matchtable to make queries in playerStandings() more concise
CREATE VIEW wintable AS
  SELECT player1 AS id, count(player1) AS wins
  FROM matches
  GROUP BY player1;

CREATE VIEW matchtable AS
  SELECT id, count(id) AS matches
  FROM players, matches
  WHERE players.id = player1 OR players.id = player2
  GROUP BY id;
