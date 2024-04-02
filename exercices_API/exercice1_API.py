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