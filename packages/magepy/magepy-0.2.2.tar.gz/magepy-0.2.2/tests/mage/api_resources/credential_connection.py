from .abstract import *
from .. import schema

class CredentialConnection( MutableAPIResource ):
    """
    Connection between an asset and a credential.

    Attributes:
        asset_id (str): ID of the associated asset
        created_at (str): When the connection was created (e.g., '2020-01-02T03:04:56.789Z')
        credential_id (str): ID of the associated credential
        id (str): Unique connection ID
        updated_at (str): When the connection was last updated (e.g., '2020-01-02T03:04:56.789Z')
    """
    _UPDATE_FN = 'update_credential_connection'
    _DELETE_FN = 'delete_credential_connection'

    __field_names__ = schema.CredentialConnection.__field_names__


    @property
    def asset(self):
        """
        The associated asset.

        Returns:
            `Asset <asset.Asset>`
        """
        from .asset import Asset
        return self._nested_resource(Asset, 'asset')


    @property
    def credential(self):
        """
        The associated credential.

        Returns:
            `Credential <credential.Credential>`
        """
        from .credential import Credential
        return self._nested_resource(Credential, 'credential')
