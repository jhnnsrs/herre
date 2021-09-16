



from herre.jupy import in_notebook
from herre.grants.code.app import AuthorizationCodeGrant
from herre.grants.backend.app import BackendGrant
from herre.grants.backend.app import BackendGrant
from herre.config.model import GrantType, HerreConfig
import asyncio 
from threading import Thread
import os
import logging

logger = logging.getLogger(__name__)

class HerreError(Exception):
    pass

def newloop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()




class HerreClient:

    def __init__(self,
        config_path = "bergen.yaml",
        username: str = None,
        password: str = None,
        allow_insecure = False,
        force_async = False,
        force_sync = False,
        register = True,
        **overrides,
    ) -> None:
        """ Creates A Herre Client

        Args:
            config_path (str, optional): [description]. Defaults to "bergen.yaml".
            username (str, optional): [description]. Defaults to None.
            password (str, optional): [description]. Defaults to None.
            allow_insecure (bool, optional): [description]. Defaults to False.
            in_sync (bool, optional): Should we force an in_sync modus if an event loop is already running. Loop will be send to another thread. Defaults to True.

        Raises:
            HerreError: [description]
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as e:
            logger.info("There is no event-loop in this thread. Lets create a new One")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if not force_async and loop.is_running() and in_notebook() :
            # Jupyter handles the eventloop a bit erradically put has top_level await, so we
            # can either have sync or non_sync code, as long as await is not a standard
            # we will use sync_mode for jupyter

            # If we are already in an event loop we are creating a new eventloop somewhere else
            thread_loop = asyncio.new_event_loop()
            t = Thread(target=newloop, args=(thread_loop,))
            t.start()
            logger.info("Running in Seperate Thread")
            self.loop = thread_loop
            self.sync_mode = True
        else:
            self.loop = loop
            self.sync_mode = False

        self.config_path = config_path
        self.config = HerreConfig.from_file(config_path, **overrides)

        if self.config.authorization_grant_type == GrantType.CLIENT_CREDENTIALS:
            self.grant = BackendGrant(self.config)

        elif self.config.authorization_grant_type == GrantType.AUHORIZATION_CODE:
            self.grant = AuthorizationCodeGrant(self.config)

        else:
            raise HerreError("Unknown GrantType")

        if register:
            set_current_herre(self)


    
    async def login(self, username: str = None, password: str = None):
        await self.grant.login(username=username, password=password)

    
    async def refresh(self):
        assert self.grant.can_refresh, "Grant is not able to refresh. Please login again"
        await self.grant.refresh()


    @property
    def logged_in(self):
        return self.grant.logged_in

    @property
    def headers(self, **additionals):
        assert self.grant.access_token is not None, "Access token is not set yet, please login?"
        return {"Authorization": f"Bearer {self.grant.access_token}", **additionals}




CURRENT_HERRE = None

def get_current_herre():
    global CURRENT_HERRE
    if not CURRENT_HERRE:
        CURRENT_HERRE = HerreClient()
    return CURRENT_HERRE

def set_current_herre(herre):
    global CURRENT_HERRE
    CURRENT_HERRE = herre