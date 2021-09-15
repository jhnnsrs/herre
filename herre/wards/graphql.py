

from herre.exceptions import TokenExpired
from herre.auth import HerreClient
from herre.wards.base import BaseQuery, BaseWard, WardException
import aiohttp
import logging
import re

logger = logging.getLogger(__name__)

gqlparsed_with_variables = re.compile(r"[\s]*(?P<type>subscription|query|mutation)\s*(?P<operation>[a-zA-Z]*)\((?P<arguments>[^\)]*)\)[\s]*{[\s]*(?P<firstchild>[^\(:]*).*")
gqlparser_without_variables = re.compile(r"[\s]*(?P<type>subscription|query|mutation)\s*(?P<operation>[a-zA-Z]*)[\s]*{[\s]*(?P<firstchild>[^\(\{\s:]*).*")

class GQLException(Exception):
    pass



class ParsedQuery(BaseQuery):

    def __init__(self, query: str) -> None:
        self.query = query
        self.variables = None
        self._type = None
        self.m = gqlparsed_with_variables.match(self.query)
        self.has_variables = True
        
        if not self.m:
            self.m = gqlparser_without_variables.match(self.query)
            self.has_variables = False

        if not self.m: raise GQLException(f"Illformed request {self.query}")


    def get_operation_name_for_datakey(self, key):
        #TODO: Make work
        return key

    def combine(self, variables: dict):
        self.variables = variables
        return {"query": self.query, "variables": self.variables}
        
    def parsed(self):
        assert self.variables and self.query, "Please specify query and set variables before parsing"
        return {"query": self.query, "variables": self.variables}

    @property
    def firstchild(self):
        return self.m.group("firstchild")

    @property
    def operation_name(self):
        return self.m.group("operation")

    @property
    def type(self):
        return self.m.group("type")

    def extract(self, result: dict):
        assert self.firstchild in result, f"Cannot Access {self.firstchild}: in {result}"
        assert result[self.firstchild] is not None, f"Empty response {result}"
        return result[self.firstchild]


class GraphQLException(WardException):
    pass

class GraphQLQueryException(GraphQLException):
    pass

class GraphQLProtocolException(WardException):
    pass


class GraphQLWard(BaseWard):

    class Meta:
        abstract = True


    def __init__(self, herre: HerreClient, endpoint: str) -> None:
        super().__init__(herre)
        self.endpoint = endpoint


    async def connect(self):
        if not self.herre.logged_in:
            await self.herre.login()

            
        self.async_session = aiohttp.ClientSession(headers=self.herre.headers)

    async def disconnect(self):
        await self.async_session.close()

    
    async def run(self, gql: ParsedQuery, variables: dict = {}):
        try:
            async with self.async_session.post(self.endpoint, json={"query": gql.query, "variables": variables}) as resp:
                
                if resp.status == 200:
                    result = await resp.json() 
                    logger.debug(f"Received Reply {result}")

                    if "errors" in result:
                        raise GraphQLQueryException(f"Ward {self.endpoint}:" + str(result["errors"]))

                    return result["data"]
                
                if resp.status == 403:
                    logger.error("Auth token is expired trying to refresh")
                    raise TokenExpired("Token Expired Error")

                if resp.status == 400:
                    raise GraphQLProtocolException(await resp.json())

                raise GraphQLProtocolException(f"Unexpected statuscode {resp.status} {resp}")


        except aiohttp.client_exceptions.ClientOSError as e :
            await self.disconnect()
            raise GraphQLProtocolException("Ward is not reachable") from e


