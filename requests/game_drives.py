from data_retriever_service.service import RetrieverService
from data_pusher_service.postgres_service import PusherService
from data_transformer_service.service import TransformService


class GameDrivesRequestService():
    def GetGameDrivesData(self):
        endpoint = 'drives'
        params = {"year": 2023,
                  "seasonType": "both",
                  "classification": "fbs"}

        data = RetrieverService.getPostgresConnection(endpoint, params)
        df = TransformService.dataframeTransform(data)
        table_name = PusherService.createPostgresTable(df, endpoint)

        PusherService.pushToPostgres(df, table_name)
        PusherService.cleansePostgresData(df, table_name)
