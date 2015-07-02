-- Table definitions for the tournament project.

-- 1. Start clean and delete tournament database if allready exists
DROP DATABASE tournament;

-- 2. Create database
CREATE DATABASE tournament;

-- 3. Connect to the database
\c tournament

-- 4. Create players Table
CREATE TABLE players (
  id serial primary key,
  name text
);

-- 5. Create matches Table, tied defines tied (true) or nontied match (false)
CREATE TABLE matches (
  player1 integer references players(id),
  player2 integer references players(id),
  tied boolean not null default false
);

-- 6. Create views: wintable and matchtable to make queries in playerStandings() more concise
create view wintable AS
  SELECT player1 as id, count(player1) as wins
  FROM matches
  GROUP BY player1;

create view matchtable AS
  SELECT id, count(id) as matches
  FROM players, matches
  WHERE players.id = player1 OR players.id = player2
  GROUP BY id;
