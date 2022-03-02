from fakts.fakts import Fakts, current_fakts
from herre.herre import Herre
from herre.fakts.config import HerreConfig
from herre.fakts.registry import GrantRegistry, get_current_grant_registry


class FaktsHerre(Herre):
    def __init__(
        self,
        *args,
        fakts: Fakts = None,
        grant_registry: GrantRegistry = None,
        fakts_key="herre",
        token_file=None,
        **kwargs
    ) -> None:
        super().__init__(*args, token_file=token_file, **kwargs)
        self._grant_registry = grant_registry or get_current_grant_registry()
        self._fakts = fakts or current_fakts.get()
        self.config = None
        self._fakts_key = fakts_key

    def configure(self, config: HerreConfig) -> None:
        self.base_url = config.base_url
        self.client_id = self.client_id or config.client_id
        self.client_secret = self.client_secret or config.client_secret
        self.token_file = self.token_file or config.token_file

        self.grant = self.grant or self._grant_registry.get_grant_for_type(
            config.authorization_grant_type
        )(**config.grant_kwargs)

        self.configured = True
        self.config = config

    async def alogin(self, **kwargs):

        if not self.config:
            self.fakts = await self._fakts.aget(self._fakts_key)
            self.configure(HerreConfig(**self.fakts))

        return await super().alogin(**kwargs)
