from data_retriever_service.service import RetrieverService
from data_pusher_service.postgres_service import PusherService
from data_transformer_service.service import TransformService


class TeamsRequestService():

    def GetTeamsData(self):
        endpoint = 'teams'
        params = {}

        data = RetrieverService.getPostgresConnection(endpoint, params)
        df = TransformService.dataframeTransform(data)
        table_name = PusherService.createPostgresTable(df, endpoint)

        PusherService.pushToPostgres(df, table_name)
        PusherService.cleansePostgresData(df, table_name)
