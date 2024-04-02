from nba_api.stats.static import teams
import matplotlib.pyplot as plt
import pandas as pd



def one_dict(list_dict):
    keys=list_dict[0].keys()
    out_dict={key:[] for key in keys}
    for dict_ in list_dict:
        for key, value in dict_.items():
            out_dict[key].append(value)
    return out_dict


# The method get_teams() returns a list of dictionaries.
nba_teams = teams.get_teams()
#print(nba_teams)
#print(len(nba_teams))

# The dictionary key id has a unique identifier for each team as a value. Let's look at the first three elements of the list:
nba_teams[0:3]
#print(nba_teams)


# To make things easier, we can convert the dictionary to a table. First, we use the function one dict, to create a dictionary. 
# We use the common keys for each team as the keys, the value is a list; each element of the list corresponds to the values for each team. We then convert the dictionary to a dataframe, each row contains the information 
# for a different team.
dict_nba_team=one_dict(nba_teams)
df_teams=pd.DataFrame(dict_nba_team)
print(df_teams.head())


# Will use the team's nickname to find the unique id, we can see the row that contains the warriors by using the column nickname as follows:
df_warriors=df_teams[df_teams['nickname']=='Warriors']
print(df_warriors)



# We can use the following line of code to access the first column of the DataFrame:
id_warriors=df_warriors[['id']].values[0][0]
# we now have an integer that can be used to request the Warriors information 
print(id_warriors)


#The function "League Game Finder " will make an API call, it's in the module stats.endpoints.
from nba_api.stats.endpoints import leaguegamefinder


#The parameter team_id_nullable is the unique ID for the warriors. Under the hood, the NBA API is making a HTTP request.
#The information requested is provided and is transmitted via an HTTP response this is assigned to the object game finder.

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=id_warriors)


# We can see the json file by running the following line of code.
gamefinder.get_json()



# The game finder object has a method get_data_frames(), that returns a dataframe. If we view the dataframe, we can see it contains information about all the games the Warriors played.
# The PLUS_MINUS column contains information on the score, if the value is negative, the Warriors lost by that many points, if the value is positive, the warriors won by that amount of points.
# The column MATCHUP has the team the Warriors were playing, GSW stands for Golden State Warriors and TOR means Toronto Raptors. vs signifies it was a home game and the @ symbol means an away game.
games = gamefinder.get_data_frames()[0]
print(games.head())

# You can download the dataframe from the API call for Golden State and run the rest like a video.
import requests

filename = "https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/PY0101EN/Chapter%205/Labs/Golden_State.pkl"

def download(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)

#download(filename, "Golden_State.pkl")

file_name = "Golden_State.pkl"
games = pd.read_pickle(file_name)
print(games.head())


# We can create two dataframes, one for the games that the Warriors faced the raptors at home, and the second for away games.

games_home=games[games['MATCHUP']=='GSW vs. TOR']
games_away=games[games['MATCHUP']=='GSW @ TOR']

# We can calculate the mean for the column PLUS_MINUS for the dataframes games_home and  games_away:
print(games_home['PLUS_MINUS'].mean())
print(games_away['PLUS_MINUS'].mean())

# We can plot out the PLUS MINUS column for the dataframes games_home and  games_away. We see the warriors played better at home.
fig, ax = plt.subplots()

games_away.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
games_home.plot(x='GAME_DATE',y='PLUS_MINUS', ax=ax)
ax.legend(["away", "home"])
plt.show()

# Calculate the mean for the column PTS for the dataframes games_home and  games_away:
print(games_home['PTS'].mean())
print(games_away['PTS'].mean())