from data_retriever_service.service import RetrieverService
from data_pusher_service.psql_service import PusherService
from data_transformer_service.servicce import DataTransform
import pandas as pd

# SET PARAMS #
endpoint = 'drives'
params =    {"year": 2023,
             "seasonType": "both",
             "classification": "fbs"}

data = RetrieverService.getConnection(endpoint, params)
df_game_drives = DataTransform.responseToDataframe(data)
df_game_drives = df_game_drives.drop(['offense_conference', 'defense_conference', 'start_time', 'end_time', 'elapsed'], axis=1)
PusherService.pushToPostgres(df_game_drives, 'd_game_drives')
