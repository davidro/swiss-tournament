-- Table definitions for the tournament project.
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.


-- 0. Create and connect to database tournament via psql command in terminal:
-- psql
-- CREATE DATABASE tournament;
-- \c tournament

-- 1. Create Tables
CREATE TABLE players (
  id serial primary key,
  name text
);

CREATE TABLE matches (
  winner integer references players(id),
  loser integer references players(id)
);

-- 2. Import This Script
-- \i tournament.sql
