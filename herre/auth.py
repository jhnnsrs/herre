



from herre.wrap_qt import wrap_qt_in_loop
from herre.logging import setLogging
from herre.jupy import in_notebook
from herre.grants.code.app import AuthorizationCodeGrant
from herre.grants.backend.app import BackendGrant
from herre.grants.backend.app import BackendGrant
from herre.config.herre import GrantType, HerreConfig
import asyncio 
from threading import Thread
import os
import logging
from herre.loop import loopify

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
        qt = None,
        auto_login=True,
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

        self.loop = None
        self.thread_id = None
        self.config_path = config_path

        setLogging(config_path=config_path)

        self.config = HerreConfig.from_file(config_path, **overrides)

        try:
            loop = asyncio.get_running_loop()
            if loop.is_running():
                logger.info("We are in an already running async loop!")
                if in_notebook():
                    logger.info("We are running in a notebook! Choosing on saved preference!")
                    if self.config.jupyter_sync:
                        thread_loop = asyncio.new_event_loop()
                        t = Thread(target=newloop, args=(thread_loop,))
                        t.start()
                        logger.info("Running in Seperate Thread so that we can use the sync syntax")
                        self.loop = thread_loop
                    else:
                        self.loop = loop
                else:
                    logger.info("We are now running in an async Context")
                    self.loop = loop
            else:
                if qt is not None:
                    logger.info("Wrapping Qt app so that we can call functions asynchronously")
                    self.loop = wrap_qt_in_loop(qt)

                self.loop = loop

        except RuntimeError as e:
            logger.info("There is no event-loop in this thread. Lets create a new One")
            if force_sync:
                thread_loop = asyncio.new_event_loop()
                t = Thread(target=newloop, args=(thread_loop,))
                t.start()
                logger.info("Running in Seperate Thread so that we can use the sync syntax")
                self.loop = thread_loop
            else:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                self.loop = loop

        if self.config.authorization_grant_type == GrantType.CLIENT_CREDENTIALS:
            self.grant = BackendGrant(self.config)

        elif self.config.authorization_grant_type == GrantType.AUHORIZATION_CODE:
            self.grant = AuthorizationCodeGrant(self.config)

        else:
            raise HerreError("Unknown GrantType")

        if register:
            set_current_herre(self)

        if auto_login:
            self.login(username=username, password=password)


    def login(self, username: str = None, password: str = None):
        self.grant.login(username=username, password=password)

    
    async def refresh(self):
        assert self.grant.can_refresh, "Grant is not able to refresh. Please login again"
        await self.grant.refresh()


    @property
    def logged_in(self):
        return self.grant.logged_in

    @property
    def user(self):
        assert self.grant.logged_in, "User is not logged in"
        return self.grant.user

    @property
    def headers(self, **additionals):
        assert self.grant.access_token is not None, "Access token is not set yet, please login?"
        return {"Authorization": f"Bearer {self.grant.access_token}", **additionals}




CURRENT_HERRE = None

def get_current_herre(**kwargs):
    global CURRENT_HERRE
    if not CURRENT_HERRE:
        CURRENT_HERRE = HerreClient(**kwargs)
    return CURRENT_HERRE

def set_current_herre(herre):
    global CURRENT_HERRE
    CURRENT_HERRE = herre