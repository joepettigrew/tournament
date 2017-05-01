-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create database called tournament
CREATE DATABASE tournament;

-- Create Players table
CREATE TABLE players (
  player_id serial NOT NULL PRIMARY KEY,
  player_name VARCHAR(255),
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Players table
CREATE TABLE matches (
  match_id serial NOT NULL PRIMARY KEY,
  winner BOOLEAN NOT NULL,
  player_id INT NOT NULL references players(player_id),
  date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
