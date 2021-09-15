import asyncio
from typing import Dict, Type
from herre.auth import get_current_herre
from herre.wards.base import BaseWard


class NoWardRegistered(Exception):
    pass



class WardRegistry:

    def __init__(self) -> None:
        self.keyWardClassMap: Dict[str, Type[BaseWard]] = {}
        self.keyInstanceMap: Dict[str, BaseWard] = {}

    def register_ward(self, identifier, wardClass: Type[BaseWard]):
        assert identifier not in self.keyWardClassMap, "We cannot register another Ward for this key"
        self.keyWardClassMap[identifier] = wardClass

    def get_ward(self, identifier) -> BaseWard:
        try:
            return self.keyWardClassMap[identifier]
        except KeyError as e:
            raise NoWardRegistered(f"No Structure registered for identifier {identifier}") from e

    def get_ward_instance(self, key) -> BaseWard:
        if key in self.keyInstanceMap: return self.keyInstanceMap[key]
        self.keyInstanceMap[key] = self.keyWardClassMap[key](get_current_herre())
        return self.keyInstanceMap[key]


    # Handling Connection

    async def connect_all(self):
        unconnected_wards = [ward for key, ward in self.keyInstanceMap.items() if not ward.connected]
        await asyncio.gather(*[ward._connect() for ward in unconnected_wards]) 

    async def unconnect_all(self):
        connected_wards = [ward for key, ward in self.keyInstanceMap.items() if ward.connected]
        await asyncio.gather(*[ward._disconnect() for ward in connected_wards])



    




WARD_REGISTRY = None

def get_ward_registry():
    global WARD_REGISTRY
    if not WARD_REGISTRY:
        WARD_REGISTRY = WardRegistry()
    return WARD_REGISTRY