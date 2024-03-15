from data_retriever_service.service import RetrieverService
from data_pusher_service.psql_service import PusherService
from data_transformer_service.servicce import DataTransform
import pandas as pd

# SET PARAMS #
endpoint = 'drives'
params =    {"year": 2023,
             "seasonType": "both",
             "classification": "fbs"}

weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
for week in weeks:

  endpoint = 'plays'
  params =    {"seasonType": "both",
              "year": 2023,
              "week":1,
              "classification": "fbs"}

  data = RetrieverService.getConnection(endpoint, params)
  df_plays = GamesTransform.responseToDataframe(data)
  df_plays = df_plays.drop(['offense_conference', 'defense_conference', 'clock'], axis=1)
  PusherService.pushToPostgres(df_plays, 'd_plays')     
