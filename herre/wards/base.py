from abc import abstractmethod
from herre.herre import Herre
from herre.wards.variables import parse_variables
from herre import get_current_herre
import asyncio
from koil import Koil, get_current_koil
from fakts import Fakts, get_current_fakts, Config
from koil.loop import koil

class WardException(Exception):
    pass

class WardMeta(type):
    """
    
    """
    def __init__(self, name, bases, attrs):
        super(WardMeta, self).__init__(name, bases, attrs)
        if attrs["__qualname__"] != "BaseWard":
            # This gets allso called for our Baseclass which is abstract
            meta = attrs["Meta"] if "Meta" in attrs else None
            assert meta is not None, f"Please provide a Meta class in your Arnheim Model {name}"

            try:
                if meta.abstract:
                    return
            except:
                pass

            register = getattr(meta, "register", True)

            if register:
                from herre.wards.registry import get_ward_registry
                key = getattr(meta, "key", None)
                assert key is not None, f"Please provide key in your Meta class to register the Ward {attrs['__qualname__']}, or specifiy register=False"
                get_ward_registry().register_ward(key, self)



class BaseQuery(object):
    """Query
    
    A query is an instructional set of how to retrieve data from a Server through a ward. A Ward takes a query populates it with credentials through
    herre and send its to its respective instance. 

    We ship with a Standard GraphQL Query.

    This can be used as a mixin for typesaftey
    
    
    
    """


class BaseWard(metaclass=WardMeta):
    """Ward

    Wards are connectors between Models and there Corresponding Endpoints (Servers). They are automatically registered in a common ward registry
    so models can just specify the ward they want to use by referencing it in their Meta 

    Args:
        BaseModel ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to ModelMeta.

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """
    id: str
    configClass = Config

    def __init__(self, *args,  herre: Herre = None, koil: Koil = None, fakts: Fakts = None, max_retries = 4, **kwargs) -> None:
        self.herre = herre or get_current_herre()
        self.koil = koil or get_current_koil()
        self.fakts = fakts or get_current_fakts()
        self.connected = False
        self.transcript = None
        self.config = None
        self.max_retries = max_retries
        super().__init__()

    @abstractmethod
    async def handle_run(self, query: BaseQuery, parsed_variables: dict):
        raise NotImplementedError("Your Ward must overwrite run")

    @abstractmethod
    async def handle_connect(self):
        raise NotImplementedError("Your Ward must overwrite run")

    @abstractmethod
    async def handle_disconnect(self):
        raise NotImplementedError("Your Ward must overwrite run")


    async def negotiate(self):
        """Negotiation is a step before launching the first query to your backend service,
        it allows for initial configurations to be transfer
        """
        return None


    async def arun(self, query: BaseQuery, variables: dict = {}):
        assert isinstance(query, BaseQuery), "Query must be of type BaseQuery"
        if not self.connected:
            await self.aconnect()

        return await self.handle_run(query, await parse_variables(variables))


    def run(self, query: BaseQuery, variables: dict = {}):
        return koil(self.arun(query, variables))


    async def adisconnect(self):  
        print("Doind this here")      
        await self.handle_disconnect()
        self.transcript = None
        self.connected = False

    async def aconnect(self): 
        if not self.fakts.loaded:
            await self.fakts.aload()


        if not self.herre.logged_in:
            await self.herre.login()

        self.config = self.configClass.from_fakts(fakts=self.fakts)
        await self.handle_connect()
        self.connected = True
        self.transcript = await self.negotiate()
        
        


    class Meta:
        abstract = True





