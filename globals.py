'''Store global variables.'''
import pandas as pd
from datetime import datetime, timedelta

today_str = datetime.utcnow().date().strftime("%Y-%m-%d")
last_update_str = pd.read_csv("homeruns.csv").tail(1).date.values[0]
homeruns_df = pd.read_csv('homeruns.csv')
players_df = pd.read_csv("players_tracked.csv", index_col=False)
teams_df = pd.read_csv("teams_info.csv", index_col=0)