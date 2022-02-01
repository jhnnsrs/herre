from herre.herrenew import Herre
from herre.fakts.config import HerreConfig
from fakts import Fakts
from herre.fakts.registry import GrantRegistry


class FaktsHerre(Herre):
    def __init__(self, fakts: Fakts, grant_registry: GrantRegistry, **kwargs) -> None:
        super().__init__(**kwargs)
        self._grant_registry = grant_registry
        self._fakts = fakts
        self.configured = False

    async def configure(self, **kwargs) -> None:
        config = await HerreConfig.from_fakts(fakts=self.fakts)

        self.client_id = self.client_id or config.client_id
        self.client_secret = self.client_secret or config.client_secret

        self.grant = self.grant or self._grant_registry.get_grant_for_type(
            config.authorization_grant_type
        )

        self.configured = True

    async def login(self, **kwargs):
        if not self.configured:
            await self.configure()

        return super().login(**kwargs)
