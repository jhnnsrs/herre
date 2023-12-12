from .base import BaseOauth2Grant
import logging


logger = logging.getLogger(__name__)


def build_authorize_url(grant: BaseOauth2Grant) -> str:
    """Builds the authorize url for the given grant.

    Parameters
    ----------
    grant : BaseOauth2Grant
        A BaseOauth2Grant

    Returns
    -------
    str
        The authorize url
    """
    return (
        f"{grant.base_url}/{grant.authorize_path}/"
        if grant.append_trailing_slash
        else f"{grant.base_url}/{grant.authorize_path}"
    )


def build_token_url(grant: BaseOauth2Grant) -> str:
    """Builds the token url for the given grant.

    Parameters
    ----------
    grant : BaseOauth2Grant
        BaseOauth2Grant

    Returns
    -------
    str
        The token url
    """
    return (
        f"{grant.base_url}/{grant.token_path}/"
        if grant.append_trailing_slash
        else f"{grant.base_url}/{grant.token_path}"
    )


def build_refresh_url(grant: BaseOauth2Grant) -> str:
    """Builds the token url for the given grant.

    Parameters
    ----------
    grant : BaseOauth2Grant
        BaseOauth2Grant

    Returns
    -------
    str
        The token url
    """
    return (
        f"{grant.base_url}/{grant.refresh_path}/"
        if grant.append_trailing_slash
        else f"{grant.base_url}/{grant.refresh_path}"
    )
