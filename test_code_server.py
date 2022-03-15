from herre.herre import Herre
from herre.grants.code_server import AuthorizationCodeServerGrant

x = Herre(
    base_url="http://localhost:8000/o",
    grant=AuthorizationCodeServerGrant(),
    client_id="UGqhHa2OS8NmTRjkVg8WKOWczYqkDVuK61yCueuO",
    client_secret="3oosB6FoC2iGASI8tkN16S8mPtlIvhqetvG5EOOJcLkn3txggTRxdp35G23CkNmvEY6fQXIXHaSzTa9Jb5Rk1hxWx0Fey0iUeOv2ZN568Z9z14kUbUbm4QQ1nacUW1gD",
)

with x:
    x.get_token()
