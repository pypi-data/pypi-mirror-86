from .abstract import *
from .. import schema

class Credential( ListableAPIResource, MutableAPIResource ):
    """
    Attributes:
        created_at (str): When the credential was created (e.g., '2020-01-02T03:04:56.789Z')
        domain (str):
        hashes (list of :class:`mage.schema.HashPair`):
        id (str): Unique credential ID
        name (str):
        password (str):
        updated_at (str): When the credential was last updated (e.g., '2020-01-02T03:04:56.789Z')
        username (str):
    """

    _GET_FN    = 'get_credential'
    _LIST_FN   = 'list_credentials'
    _SEARCH_FN = 'search_credentials'
    _UPDATE_FN = 'update_credential'
    _DELETE_FN = 'delete_credential'

    __field_names__ = schema.Credential.__field_names__
