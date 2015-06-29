-- Table definitions for the tournament project.

-- 1. Start clean and delete tournament database if allready exists
-- DROP DATABASE tournament;

-- 2. Create database
-- CREATE DATABASE tournament;

-- 3. Connect to the database
-- \c tournament

-- 4. Import This Script
-- \i tournament.sql


-- Create players and matches Tables
CREATE TABLE players (
  id serial primary key,
  name text
);

CREATE TABLE matches (
  player1 integer references players(id),
  player2 integer references players(id),
  outcome text default 'nontied' check (outcome = 'nontied' OR outcome = 'tied' )
);

-- Create view that contains the number of players currently registered
create view players_num AS
  SELECT COUNT(*) as num from players;
