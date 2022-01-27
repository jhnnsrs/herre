from asyncio.tasks import create_task
from typing import Dict
import websockets
import json
import asyncio
from arkitekt.config import ArkitektConfig
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedError,
    ConnectionClosedOK,
)
from arkitekt.messages.base import MessageDataModel
from arkitekt.transport.postman.websocket import DefiniteConnectionFail
from fakts.config.base import Config
from fakts.fakts import Fakts, get_current_fakts
from herre.herre import Herre, get_current_herre
from herre.wards.base import BaseWard
from herre.wards.graphql import ParsedQuery
from herre.wards.query import get_schema_registry
from herre.wards.variables import parse_variables
from koil.koil import Koil, get_current_koil
import logging
import uuid

logger = logging.getLogger(__name__)


GQL_WS_SUBPROTOCOL = "graphql-ws"

# all the message types
GQL_CONNECTION_INIT = "connection_init"
GQL_START = "start"
GQL_STOP = "stop"
GQL_CONNECTION_TERMINATE = "connection_terminate"
GQL_CONNECTION_ERROR = "connection_error"
GQL_CONNECTION_ACK = "connection_ack"
GQL_DATA = "data"
GQL_ERROR = "error"
GQL_COMPLETE = "complete"
GQL_CONNECTION_KEEP_ALIVE = "ka"


class CorrectableConnectionFail(Exception):
    pass


class DefiniteConnectionFail(Exception):
    pass


class InvalidPayload(Exception):
    pass


class GraphQLWebsocketSession:
    def __init__(
        self, fakts: Fakts = None, herre: Herre = None, koil: Koil = None
    ) -> None:
        self.herre = herre or get_current_herre()
        self.koil = koil or get_current_koil()
        self.fakts = fakts or get_current_fakts()

        self.connection_initialized = False

        self.ongoing_subscriptions: Dict[str, asyncio.Queue] = {}
        pass

    async def aforward(self, message):
        await self.send_queue.put(message)

    async def aconnect(self):
        if not self.fakts.loaded:
            await self.fakts.aload()

        self.config = await ArkitektConfig.from_fakts(self.fakts)

        if not self.herre.logged_in:
            await self.herre.alogin()

        self.send_queue = asyncio.Queue()
        self.connection_task = create_task(self.websocket_loop())

    async def adisconnect(self):
        self.connection_task.cancel()

        try:
            await self.connection_task
        except asyncio.CancelledError:
            logger.info(f"Websocket Transport {self} succesfully disconnected")

    async def websocket_loop(self, retry=0):
        send_task = None
        receive_task = None
        self.connection_initialized = False
        try:
            try:
                async with websockets.connect(
                    f"ws://{self.config.host}:{self.config.port}/graphql?token={self.herre.state.access_token}",
                    subprotocols=[GQL_WS_SUBPROTOCOL],
                ) as client:

                    send_task = create_task(self.sending(client))
                    receive_task = create_task(self.receiving(client))

                    self.connection_alive = True
                    self.connection_dead = False
                    done, pending = await asyncio.wait(
                        [send_task, receive_task],
                        return_when=asyncio.FIRST_EXCEPTION,
                    )
                    self.connection_alive = True

                    for task in pending:
                        task.cancel()

                    for task in done:
                        raise task.exception()

            except ConnectionClosedError as e:
                logger.exception(e)
                raise CorrectableConnectionFail from e

            except Exception as e:
                logger.warning(
                    "THIS EXCEPTION HAS NO RETRY STRATEGY... TRYING TO RETRY??"
                )
                print(e)
                raise CorrectableConnectionFail from e

        except CorrectableConnectionFail as e:
            logger.info(f"Trying to Recover from Exception {e}")
            if retry > self.retries:
                raise DefiniteConnectionFail("Exceeded Number of Retries")
            await asyncio.sleep(self.time_between_retries)
            logger.info(f"Retrying to connect")
            await self.websocket_loop(retry=retry + 1)

        except DefiniteConnectionFail as e:
            self.connection_dead = False
            raise e

        except asyncio.CancelledError as e:
            logger.info("Got Canceleld")
            if send_task and receive_task:
                send_task.cancel()
                receive_task.cancel()

            cancellation = await asyncio.gather(
                send_task, receive_task, return_exceptions=True
            )
            raise e

    async def sending(self, client, headers=None):
        payload = {"type": GQL_CONNECTION_INIT, "payload": {"headers": headers}}
        await client.send(json.dumps(payload))

        try:
            while True:
                message = await self.send_queue.get()
                logger.debug("GraphQL Websocket: >>>>>> " + message)
                await client.send(message)
                self.send_queue.task_done()
        except asyncio.CancelledError as e:
            logger.debug("Sending Task sucessfully Cancelled")

    async def receiving(self, client):
        try:
            async for message in client:
                logger.debug("Postman Websocket: <<<<<<< " + message)
                await self.broadcast(message)
        except asyncio.CancelledError as e:
            logger.debug("Receiving Task sucessfully Cancelled")

    async def broadcast(self, res):
        print(res)
        try:
            message = json.loads(res)
        except json.JSONDecodeError as err:
            logger.warning(
                "Ignoring. Server sent invalid JSON data: %s \n %s", res, err
            )

        type = message["type"]

        if type == GQL_CONNECTION_KEEP_ALIVE:
            return

        if type in [GQL_DATA, GQL_COMPLETE]:

            if "id" not in message:
                raise InvalidPayload(f"Protocol Violation. Expected 'id' in {message}")

            id = message["id"]
            assert (
                id in self.ongoing_subscriptions
            ), "Received Result for subscription that is no longer or was never active"
            await self.ongoing_subscriptions[id].put(message)

        print(message)

    async def subscribe(
        self,
        gql: ParsedQuery,
        variables: dict = {},
        retry=0,
        headers=None,
    ):
        variables, files = await parse_variables(variables)

        assert gql.type == "subscription", "Only Subscriptions are allowed"
        assert not files, "We cannot send files through websockets"

        id = str(uuid.uuid4())
        subscribe_queue = asyncio.Queue()
        self.ongoing_subscriptions[id] = subscribe_queue

        payload = {"headers": headers, "query": gql.query, "variables": variables}
        frame = {"id": id, "type": GQL_START, "payload": payload}
        await self.aforward(json.dumps(frame))
        print("hallo")

        while True:
            answer = await subscribe_queue.get()

            if answer["type"] == GQL_DATA:
                payload = answer["payload"]

                if "data" in payload:
                    yield await get_schema_registry().expand_from_schema(
                        "arkitekt", gql, payload["data"]
                    )

            if answer["type"] == GQL_COMPLETE:
                print("Subcription done")
                return
