-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Create a database named tournament
create Database tournament;
--Create a connection to the database tournament
\c tournament
--Create a table for players
create table players (pid serial primary key, name text);
--Create a table for matches
create table matches(mid serial primary key, winner integer references players(pid), loser integer references players(pid));

