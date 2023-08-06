# coding: utf-8

__all__ = ['StreamingConnectionConfiguration']

import socket


class StreamingConnectionConfiguration(object):
    """ This class is designed for store the stream connection configuration
            The configuration will be difference for each communication protocol.
            ie. Electron websocket using Open Message Model (OMM), QPS Streaming Beta or Generic RDP Streaming.
    """

    class StreamReconnectionConfiguration(object):
        """ This class is designed to handle the websocket reconnection configuration """

        #   default delay time before do a reconnection in secs
        _DefaultReconnectionDelayTime_secs = 5

        #   default reset the reconnection time after last requested uri
        _DefaultResetReconnectionTime_secs = 120.0

        def __init__(self, websocket_endpoints, secure=True):
            assert len(websocket_endpoints) > 0
            #   store all of possible websocket endpoints
            self._websocket_endpoints = websocket_endpoints
            self._secure = secure

            #   store the current reconnection configuration
            self._num_reconnection = 0
            self._reconnection_delay_secs = 0

            #   current websocket endpoint index
            self._current_websocket_endpoint_index = 0
            self._start_websocket_endpoint_index = 0

            #       store the last requested websocket uri 
            # self._last_requested_uri = None

        @property
        def secure(self):
            return self._secure

        @secure.setter
        def secure(self, secure):
            self._secure = secure
            #   reset config
            self.reset()

        @property
        def websocket_endpoints(self):
            return self._websocket_endpoints

        @websocket_endpoints.setter
        def websocket_endpoints(self, websocket_endpoints):
            self._websocket_endpoints = websocket_endpoints
            #   reset config
            self.reset()

        @property
        def uris(self):
            return [self._build_websocket_uri(websocket_endpoint, self.secure)
                    for websocket_endpoint in self._websocket_endpoints]

        @property
        def reconnection_delay_secs(self):
            return self._reconnection_delay_secs

        def initialize_websocket_uri(self):
            assert len(self._websocket_endpoints) > 0
            return self._build_websocket_uri(self._websocket_endpoints[0], self._secure)

        def next_websocket_uri(self):
            """ This function is used to get next available websocket uri.
                    This function also calculate the waiting time and count the number of reconnection if it still doesn't successful
            """

            #   get number of websocket endpoints
            num_websocket_endpoints = len(self._websocket_endpoints)

            #   construct uri from websocket list
            self._current_websocket_endpoint_index = (self._current_websocket_endpoint_index + 1) % num_websocket_endpoints
            websocket_uri = self._build_websocket_uri(self._websocket_endpoints[self._current_websocket_endpoint_index],
                                                      self._secure)

            # #   do an intelligence reset
            # current_time = time.time()
            # if self._last_requested_uri and \
            #     current_time > self._last_requested_uri + self._DefaultResetReconnectionTime_secs:
            # #   this request is too long since last request, so reset the reconnection delay time and number of reconnection
            #     self.reset()

            #   check for increase the reconnection delay
            if self._num_reconnection != 0 and self._num_reconnection % num_websocket_endpoints == 0:
                #   this websocket endpoint is circle around, so do a delay
                #       increase the waiting time if all websockets cannot connect
                delay_multiplier = (self._num_reconnection + 1) // num_websocket_endpoints
                self._reconnection_delay_secs = self._DefaultReconnectionDelayTime_secs * delay_multiplier
            else:
                #   it still has a websocket endpoint to try, so delay will be 0
                self._reconnection_delay_secs = 0

            #   increase counter
            self._num_reconnection += 1

            #   store the last requested uri
            # self._last_requested_uri = time.time()

            #   done
            return websocket_uri

        def reset(self):
            """ Reset the calculator for building next websocket uri """
            #   reset
            #       number of reconnection
            self._num_reconnection = 0
            #       delay
            self._reconnection_delay_secs = 0

        @staticmethod
        def _build_websocket_uri(websocket_endpoint, secure):
            return '{}://{}/WebSocket'.format('wss' if secure else 'ws', websocket_endpoint)

    def __init__(self):
        self.host = "localhost:15000"
        self.user = ""
        self.dacs_application_id = "256"
        self.deployed_platform_username = ""
        self.auth_token = None
        self.connection_retry = 5
        self._header = []
        self.login_message = None

        ############################################################
        #   stream connection auto-reconnect support

        #   list of available websocket endpoints
        self._websocket_endpoints = [self.host, ]
        #   connection type SSL or not?
        self._secure = False

        try:
            position_host = socket.gethostname()
            self._dacs_position = f"{socket.gethostbyname(position_host)}/{position_host}"
        except socket.gaierror:
            self._dacs_position = "127.0.0.1"

        #   build the stream reconnection configuration
        self._stream_reconnection_config = self.StreamReconnectionConfiguration(self._websocket_endpoints, self.secure)

        #   store the currently websocket uri
        self._uri = None

        #   call initialize function
        self._initialize()

    @property
    def header(self):
        return self._header
    @property
    def secure(self):
        return self._secure

    @secure.setter
    def secure(self, secure):
        #   check is the secure is changed or not?
        if self._secure is not secure:
            #   secure is changed, so reinitialize it
            self._secure = secure

            #   set secure to reconnection config
            self._stream_reconnection_config.secure = self._secure

            #   re-initialize websocket uri
            self._initialize()

    @property
    def websocket_endpoints(self):
        return self._websocket_endpoints

    @websocket_endpoints.setter
    def websocket_endpoints(self, websocket_endpoints):
        self._websocket_endpoints = websocket_endpoints

        #   set websocket endpoint to the reconnection config
        self._stream_reconnection_config.websocket_endpoints = websocket_endpoints

        #   re-initialize websocket uri
        self._initialize()

    @property
    def uri(self):
        return self._uri

    @property
    def uris(self):
        return self._stream_reconnection_config.uris

    @property
    def reconnection_delay_secs(self):
        return self._stream_reconnection_config.reconnection_delay_secs

    def _initialize(self):
        """ Initialize websocket uri """
        self._uri = self._stream_reconnection_config.initialize_websocket_uri()

    def set_next_available_websocket_uri(self):
        """ Set the next available websocket uri """
        #   get next websocket uri and store it
        self._uri = self._stream_reconnection_config.next_websocket_uri()

    def reset_reconnection_config(self):
        """ Reset the reconnection config """
        self._stream_reconnection_config.reset()
