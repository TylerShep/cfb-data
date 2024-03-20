from data_retriever_service.service import RetrieverService
from data_pusher_service.postgres_service import PusherService
from data_transformer_service.service import TransformService


class PlayByPlayRequestService():

    def GetGameDrivesData(self):

        for week in range(1, 16):
            endpoint = 'plays'
            params = {"seasonType": "both",
                      "year": 2023,
                      "week": week,
                      "classification": "fbs"}

            data = RetrieverService.getPostgresConnection(endpoint, params)
            df = TransformService.dataframeTransform(data)
            table_name = PusherService.createPostgresTable(df, endpoint)

            PusherService.pushToPostgres(df, table_name)
            PusherService.cleansePostgresData(df, table_name)
