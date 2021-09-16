from abc import abstractmethod
from herre.loop import loopify
from herre.wards.variables import parse_variables
from herre.auth import HerreClient
import asyncio

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

    def __init__(self, herre: HerreClient) -> None:
        self.herre = herre
        self.connected = False
        self.transcript = None
        super().__init__()

    @abstractmethod
    async def run(self, query: BaseQuery, variables: dict):
        raise NotImplementedError("Your Ward must overwrite run")

    @abstractmethod
    async def connect(self):
        raise NotImplementedError("Your Ward must overwrite run")

    @abstractmethod
    async def disconnect(self):
        raise NotImplementedError("Your Ward must overwrite run")


    async def negotiate(self):
        """Negotiation is a step before launching the first query to your backend service,
        it allows for initial configurations to be transfer
        """
        return None


    async def _run_async(self, query: BaseQuery, variables: dict):
        assert isinstance(query, BaseQuery), "Query must be of type BaseQuery"
        if not self.connected:
            await self._connect()
        return await self.run(query, await parse_variables(variables))


    def _run_sync(self, query: BaseQuery, variables: dict):
        return loopify(self._run_async(query, variables))



    async def _disconnect(self):        
        await self.disconnect()
        self.transcript = None
        self.connected = False

    async def _connect(self):        
        await self.connect()
        self.transcript = await self.negotiate()
        self.connected = True
        


    class Meta:
        abstract = True





