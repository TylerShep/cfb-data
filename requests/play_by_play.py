from data_retriever_service.service import RetrieverService
from data_pusher_service.psql_service import PusherService
from data_transformer_service.service import DataTransform
import pandas as pd

# SET PARAMS #
endpoint = 'drives'
params = {"year": 2023,
          "seasonType": "both",
          "classification": "fbs"}

weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
for week in weeks:
    endpoint = 'plays'
    params = {"seasonType": "both",
              "year": 2023,
              "week": week,
              "classification": "fbs"}

    data = RetrieverService.getConnection(endpoint, params)
    df_plays = DataTransform.responseToDataframe(data)
    df = df_plays.drop(
        ['offense_conference', 'defense_conference', 'home', 'away', 'clock', 'wallclock', 'offense_timeouts',
         'defense_timeouts'], axis=1)
    df['play_text'] = df['play_text'].fillna('')
    PusherService.pushToPostgres(df, 'd_plays')
