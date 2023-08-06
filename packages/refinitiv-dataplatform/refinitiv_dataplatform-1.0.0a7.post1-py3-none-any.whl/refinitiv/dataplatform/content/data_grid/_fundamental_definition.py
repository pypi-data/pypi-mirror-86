# coding: utf8

__all__ = ["FundamentalDefinition"]


from pandas import DataFrame
from refinitiv.dataplatform.delivery.data.endpoint import Endpoint


class FundamentalDefinition(object):

    class Data(Endpoint.EndpointData):
        def __init__(self, raw):
            super().__init__(raw)
            self._data = None

            if raw:
                self._data = raw.get("data")

        @property
        def df(self):
            data_dataframe = DataFrame(self._data)
            return data_dataframe

    class Response(Endpoint.EndpointResponse):

        def __init__(self, response):
            super().__init__(response, service_class=FundamentalDefinition)
