# ViaGolf
ViaGolf is the platform for roster management and scoring for the Viasat Golf League. It's currently built on a Docker container running a PostGres SQL DB, and some python code to query the DB, pull player and score data, and calculate results.

This is a slow work in progress, and likely done poorly :)

Roadmap:

Basic functionality - manually import player and score data for rounds played to the DB, use python program to calculate and store scores
Add python function to calculate and update player handicaps based on last XX rounds
Add python function to add or remove players from DB
Add python function to group players into teams, assign their points to team totals for the season
Set up WebUI so we have a GUI that can handle all these tasks in a pretty way

Folder structure:
Archive - Initial effort, kept for historical reasons
Standalone - Script that will take input from a yaml file and render results. Hard to keep up-to-date, but a good POC
db-connected - Current effort. Working to integrate with a DB that can be easily updated and maintain historical data