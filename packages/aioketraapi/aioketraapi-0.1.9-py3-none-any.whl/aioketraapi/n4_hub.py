from aiohttp import ClientWebSocketResponse, WSMsgType, ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from asyncio import AbstractEventLoop, iscoroutinefunction, CancelledError, TimeoutError
from aioketraapi import KeypadOperationsApi, GroupOperationsApi, ApiClient, Configuration, HubOperationsApi
from aioketraapi import WebsocketV2Notification
from aioketraapi.keypad import Keypad
from aioketraapi.group import Group
from aioketraapi.exceptions import OpenApiException

WEBSOCKET_HEARTBEAT_INTERVAL = 60.0

class N4HubWebSocketConnectionError(BaseException):
    pass

class N4HubWebSocketConnection:
    def __init__(self, api_client: ApiClient):
        self.ws = None
        self.api_client = api_client

    async def connect(self, ws_url, oauth_token):
        self.ws = await self.api_client.rest_client.client_session.ws_connect(ws_url,
                                                                              heartbeat=WEBSOCKET_HEARTBEAT_INTERVAL,
                                                                              autoping=True)
        # from https://s3.amazonaws.com/ketra-software/KetraMobileAPI/v1/KetraN4WebsocketProtocol.pdf
        msg = [0x06, 0x00, 0x0F]
        msg.append((len(oauth_token) >> 8) & 0xFF)
        msg.append(len(oauth_token) & 0xFF)
        msg.extend([b for b in oauth_token.encode('ascii')])
        await self.ws.send_bytes(bytearray(msg))

    async def close(self):
        assert self.ws is not None
        await self.ws.close()

    def __aiter__(self) -> "N4HubWebSocketConnection":
        assert self.ws is not None
        return self

    async def __anext__(self) -> WebsocketV2Notification:
        assert self.ws is not None
        while True:
            recv_msg = await self.ws.receive(timeout=WEBSOCKET_HEARTBEAT_INTERVAL*3)
            if recv_msg.type == WSMsgType.TEXT:
                model = self.api_client.deserialize(recv_msg, WebsocketV2Notification)
                return model
            elif recv_msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
                raise StopAsyncIteration  # NOQA
            else:
                # ignore this message and go back and wait for a new one
                pass



class N4Hub():

    def __init__(self, internal_ip: str, serial_number: str, installation_id: str, url_base :str, oauth_token :str,
                 loop :AbstractEventLoop=None):
        self.internal_ip = internal_ip
        self.serial_number = serial_number
        self.installation_id = installation_id
        self.url_base = url_base
        ws_url_tmp, _, _ = url_base.rpartition('/')
        self.ws_url = f"{ws_url_tmp.replace('https', 'wss')}/notifications"
        self.oauth_token = oauth_token
        self.is_local = "api.goketra.com" not in url_base
        self.client_config = Configuration()
        self.client_config.host = f"{self.url_base}/api/v1"
        self.client_config.username = "na"
        self.client_config.password = self.oauth_token
        self.client_config.loop = loop
        if self.is_local:
            self.client_config.verify_ssl = False
        self.connected_websocket = None


    @classmethod
    async def get_hub(cls, installation_id, oauth_token, use_cloud = False, loop=None):
        """
        Returns a hub for the given installation

        :param installation_id:  installation id of Design Studio installation
        :param oauth_token:      authentication token for user account
        :param use_cloud:        False: connect to hub over local network
                                 True:  connect to hub over cloud connection
        :param loop:             optional event loop to use for async operations
        :return:                 N4Hub object
        """
        query_url = f"https://my.goketra.com/api/n4/v1/query?installation_id={installation_id}"
        async with ClientSession(loop=loop) as session:
            async with session.get(query_url) as response:
                if response.status == 200:
                    hub_query_resp = await response.json()
                    if hub_query_resp['success'] == 'true' and len(hub_query_resp['content']) > 0:
                        for hub_query_entry in hub_query_resp['content']:
                            internal_ip = hub_query_entry['internal_ip']
                            serial_number = hub_query_entry['serial_number']
                            if use_cloud:
                                url = f"https://api.goketra.com/{installation_id}/{serial_number}/webAPI"
                                hub = N4Hub(internal_ip, serial_number, installation_id, url, oauth_token, loop)
                            else:
                                url = f"https://{internal_ip}/ketra.cgi"
                                hub = N4Hub(internal_ip, serial_number, installation_id, url, oauth_token, loop)
                            if await hub.test_connectivity():
                                return hub
            return None

    def create_client_session(self):
        """
        Creates and returns an ApiClient session
        """
        return ApiClient(configuration=self.client_config)


    async def test_connectivity(self, timeout=5):
        async with self.create_client_session() as api_client:
            hub_api = HubOperationsApi(api_client)
            try:
                _ = await hub_api.hub_get(_request_timeout=timeout)
                return True
            except (TimeoutError, OpenApiException, ClientConnectorError):
                return False



    async def get_keypads(self, **kwargs):
        """
        Gets the keypads from the installation
        :param kwargs: optional arguments
                       includeall (defaults to false): include cascaded keypads
                       nobuttons (defaults to false): return only keypads, not buttons
        :return: list of Keypad objects
        """
        async with self.create_client_session() as api_client:
            kp_api = KeypadOperationsApi(api_client)
            response_model = await kp_api.keypads_get(**kwargs)
            return [Keypad(keypad, self) for keypad in response_model.content]

    async def get_groups(self, include_internal=False, **kwargs):
        """
        Gets the groups in the installation
        :param include_internal: include internally-generated master groups (begin with Internal_MasterGroup)
        :param kwargs: optional arguments
                       name:  return group matching provided name
        :return: list of Group objects
        """
        async with self.create_client_session() as api_client:
            kp_api = GroupOperationsApi(api_client)
            response_model = await kp_api.groups_get(**kwargs)
            return [Group(group, self) for group in response_model.content if include_internal or 'Internal_MasterGroup' not in group.name]

    async def __create_websocket_connection(self, api_client):
        connection = N4HubWebSocketConnection(api_client)
        await connection.connect(self.ws_url, self.oauth_token)
        return connection

    async def websocket_notifications(self) -> WebsocketV2Notification:
        async with self.create_client_session() as api_client:
            ws = await self.__create_websocket_connection(api_client)
            async for notification in ws:
                yield notification


    async def register_websocket_callback(self, notify_callback):
        """
        Connects to websocket server of hub (or cloud proxy) in order to receive notifications such as
        button press notifications or group state changes through a callback method.
        Runs indefinitely until disconnect websocket is called
        :param notify_callback:   callback function or coroutine to receive notifications.
               Should take one parameter of type WebsocketV2Notification
        """
        async with self.create_client_session() as api_client:
            try:
                ws = await self.__create_websocket_connection(api_client)
                self.connected_websocket = ws
                async for notification in ws:
                    if iscoroutinefunction(notify_callback):
                        await notify_callback(notification)
                    else:
                        notify_callback(notification)
            except (ClientConnectorError, CancelledError, TimeoutError):
                raise N4HubWebSocketConnectionError()
            finally:
                self.connected_websocket = None


    async def disconnect_websocket_callback(self):
        """
        Closes a websocket connection established with register_websocket_callback
        :return:
        """
        if self.connected_websocket is not None:
            await self.connected_websocket.close()
            self.connected_websocket = None









