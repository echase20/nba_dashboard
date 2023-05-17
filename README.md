# nba_dashboard
NBA statistics dashboard leveraging Redis as the database

Here are the instructions to get the NBA dashboard up and running.
1. Start up a redis server on your machine
2. Install plotly, dash, and nba_api using pip or condo
3. In the test nba api file, there are a couple functions to run. First, run get_career_stats, this loads all player career data into the database under the key FirstnameLastNameCareer
NOTE: sometimes the api times out resulting in some players not getting loaded in, in the terminal you will see which players fail with an error message. To get all players into the database, the function might have to be run a couple of times. But, one run of the function should get enough players for testing.
4. In the test nba api file, run get_team_stats. This loads all 30 NBA teams data into the database under the key CityTeamnameStats
5. Run the NBA-Dash.py file as is and follow the link to the dashboard
