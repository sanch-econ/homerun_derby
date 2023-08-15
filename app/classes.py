import statsapi
import pandas as pd
from datetime import datetime, timedelta
from globals import *

class Schedule:

    def __init__(self, start_date : str = last_update_str, end_date : str = today_str):
        self.start_date = start_date
        self.end_date = end_date
        self.schedule = statsapi.schedule(start_date=start_date, end_date=end_date)
        self.game_info = [[game.get('game_id'), game.get('game_date')] for game in self.schedule]

    def create_hr_df(self):

        ''' Creates a dataframe of homeruns hit within schedule.
                columns : ["player_id", "homeruns", "game_id", "date"] '''

        homerun_data = []

        for game_id, game_date in self.game_info:

            game = Game(game_id, game_date)

            game_hr_data = game.extract_homerun_data()

            if len(game_hr_data) > 0:
                    for sublist in game_hr_data:
                        sublist.extend([game_id, game_date])
                        homerun_data.append(sublist)

        return pd.DataFrame(homerun_data, columns= ["player_id", "homeruns", "game_id", "date"])
    

class Game:
 
    def __init__(self, game_id, game_date):
        self.game_id = game_id
        self.date = game_date
        self.boxscore = statsapi.boxscore_data(game_id)

    def extract_homerun_data(self):
    
        '''Return list of list in which each sublist contains a player id and homeruns they hit in game.'''

        bs = self.boxscore
        
        homeruns_list = []

        away_players = [player for player in bs["away"]["players"]]
        home_players = [player for player in bs["home"]["players"]]

        for player in away_players:
            homeruns = bs["away"]["players"][f"{player}"]["stats"]["batting"].get("homeRuns")
            if homeruns is None:
                homeruns = 0
            if homeruns > 0:
                player = int(player[2:])
                homeruns_list.append([player, homeruns])

        for player in home_players:
            homeruns = bs["home"]["players"][f"{player}"]["stats"]["batting"].get("homeRuns")
            if homeruns is None:
                homeruns = 0
            if homeruns > 0:
                player = int(player[2:])
                homeruns_list.append([player, homeruns])

        return homeruns_list
    

class HomerunUpdater:
    """
    This class is used to update homeruns.csv with latest homeruns hit.
    """

    today = datetime.utcnow().date()
    
    def __init__(self):
        pass
    
    @staticmethod
    def update(hr_df) -> None:

        # Reads in prev hr_df
        prev_hr_df = homeruns_df
        
        # Combines previous homeruns with homeruns gathered now.
        hr_df = pd.concat([prev_hr_df, hr_df], ignore_index=False).drop_duplicates()

        # Saves updated homeruns df to csv.
        hr_df.to_csv("homeruns.csv", index=False)


class DataframeGenerator:
    """
    This class creates the Dataframes that will be displayed using streamlit.
    """

    def __init__(self):
        pass

    @staticmethod
    def generate(monthly = False):

        # Reads updated homeruns df to csv.
        hr_df = pd.read_csv('homeruns.csv')

        # Filters hr_df for only homeruns hit in May
        if monthly:
            month = datetime.utcnow().date().month
            hr_df = hr_df[pd.to_datetime(hr_df.date) >= datetime(2023, month, 1)]

        # Reads in players tracked csv to df
        players_tracked_df = players_df

        # Adds total homeruns hit in given period for each player tracked.
        players_tracked_df["homeruns"] = players_tracked_df.apply(lambda x: hr_df[hr_df.player_id == x.id].homeruns.sum(), axis=1)

        # Reads in teams info csv to df
        teams_info_df = teams_df

        # Creates mapping dictionary used to calculate team totals.
        mapping_dict = players_tracked_df.set_index("name")["homeruns"].to_dict()

        results_df = pd.DataFrame(teams_info_df.replace(mapping_dict).sum(axis=1).sort_values(ascending=False), columns=["Homeruns"])

        return results_df
    

    @staticmethod
    def generate_time_series():

        ''' 
        Generate time series df of homeruns hit for each team.
            - work in progress
        '''
                
        hr_df = homeruns_df

        results_df = pd.DataFrame()
        
        for date in pd.to_datetime(hr_df.date).unique():
            
            df = hr_df[pd.to_datetime(hr_df.date) < date]

            # Reads in players tracked csv to df
            players_tracked_df = players_df

            # Adds total homeruns hit in given period for each player tracked.
            players_tracked_df["homeruns"] = players_tracked_df.apply(lambda x: df[df.player_id == x.id].homeruns.sum(), axis=1)

            # Reads in teams info csv to df
            teams_info_df = teams_df

            # Creates mapping dictionary used to calculate team totals.
            mapping_dict = players_tracked_df.set_index("name")["homeruns"].to_dict()

            results_df[date] = pd.DataFrame(teams_info_df.replace(mapping_dict).sum(axis=1).sort_values(ascending=False), columns=["Homeruns"])

        return results_df
    
