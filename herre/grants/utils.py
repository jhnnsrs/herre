from herre.config import HerreConfig
from herre.herre import Herre


def build_authorize_url(herre: Herre):
    return f"{herre.base_url}/{herre.auth_path}/" if herre.append_trailing_slash else f"{herre.base_url}/{herre.auth_path}"

def build_token_url(herre: Herre):
    return f"{herre.base_url}/{herre.token_path}/" if herre.append_trailing_slash else f"{herre.base_url}/{herre.token_path}"

def build_refresh_url(herre: Herre):
    return f"{herre.base_url}/{herre.refresh_path}/" if herre.append_trailing_slash else f"{herre.base_url}/{herre.refresh_path}"
