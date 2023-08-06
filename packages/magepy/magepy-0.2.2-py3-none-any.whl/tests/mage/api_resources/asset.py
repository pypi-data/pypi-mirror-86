from .abstract import *
from .. import schema

class Asset( ListableAPIResource, MutableAPIResource ):
    """
    Attributes:
        asset_identifier (str): Identifier of the asset (e.g., '192.168.1.1')
        asset_source (mage.schema.AssetSource): How this asset was created (customer defined vs discovered)
        asset_type (mage.schema.AssetType): Type of the asset (e.g., 'IP_ADDRESS')
        created_at (str): When the asset was created (e.g., '2020-01-02T03:04:56.789Z')
        criticality (int): An integer value that represents the potential impact that the loss or compromise of the asset would have. 1 is the default (lowest) criticality.  5 is the most impactful.
        id (str): Unique asset ID
        tags (list of str): One or more labels or identifiers using arbitrary values (e.g., 'app-prod', 'app-dev', etc.)
        updated_at (str): When the asset was last updated (e.g., '2020-01-02T03:04:56.789Z')
    """

    _GET_FN    = 'get_asset'
    _LIST_FN   = 'list_assets'
    _SEARCH_FN = 'search_assets'
    _UPDATE_FN = 'update_asset'
    _DELETE_FN = 'delete_asset'
    _QUERIES   = ['by_identifier']

    __field_names__ = schema.Asset.__field_names__


    @property
    def assessments(self):
        """
        Associated assessments.

        Returns:
            `ListObject` of `AssessmentAssetConnection <assessment_asset_connection.AssessmentAssetConnection>`
        """
        from .assessment_asset_connection import AssessmentAssetConnection
        return self._nested_resource_list(AssessmentAssetConnection, 'assessments', AssessmentAssetConnection.__field_names__)


    @property
    def asset_groups(self):
        """
        Associated asset groups.

        Returns:
            `ListObject` of `AssetGroupConnection <asset_group_connection.AssetGroupConnection>`
        """
        from .asset_group_connection import AssetGroupConnection
        return self._nested_resource_list(AssetGroupConnection, 'asset_groups', AssetGroupConnection.__field_names__)


    def connect(self, item = None, assessment_id = None, asset_group_id = None):
        """
        Connect an asset to an assessment or asset group

        Args:
            item (object, optional): Assessment or AssessmentRun or AssetGroup to connect the asset to
            assessment_id (str, optional): ID of the assessment to connect the asset to
            asset_group_id (str, optional): ID of the asset group to connect the asset to

        Returns:
            `AssessmentAssetConnection <assessment_asset_connection.AssessmentAssetConnection>` or `AssetGroupConnection <asset_group_connection.AssetGroupConnection>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> asset = mage.Asset.eq(asset_identifier='www.example.com')[0]
            >>> asset.connect(mage.Assessment.last()[0])
        """

        from .assessment import Assessment
        from .assessment_asset_connection import AssessmentAssetConnection
        from .asset_group import AssetGroup
        from .asset_group_connection import AssetGroupConnection
        if isinstance(item, Assessment) or assessment_id:
            if item:
                assessment_id = item.id
            retval = self.mutate('create_assessment_asset_connection', input={'asset_id': self.id, 'assessment_id': assessment_id})
            if retval:
                retval = AssessmentAssetConnection.init(retval)
                return retval
            else:
                return None

        if isinstance(item, AssetGroup) or asset_group_id:
            if item:
                asset_group_id = item.id
            retval = self.mutate('create_asset_group_connection', input={'group_id': asset_group_id, 'asset_id': self.id})

            if retval:
                retval = AssetGroupConnection.init(retval)
                return retval
            else:
                return None

        raise TypeError("%s not supported" % type(item))


    @property
    def connections(self):
        """
        Asset relationships.

        Returns:
            `ListObject` of `AssetConnection <asset_connection.AssetConnection>`
        """
        from .asset_connection import AssetConnection
        return self._nested_resource_list(AssetConnection, 'connections', AssetConnection.__field_names__)


    @classmethod
    def create(cls, asset_type, id, **kwargs):
        """
        Creates a new asset.

        Args:
            asset_type (mage.schema.AssetType): Type of asset to create
            id (str): Asset identifier
            **kwargs: Additional arguments to initialize the asset with.

        Returns:
            `Asset <asset.Asset>`: The created asset

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Asset.create('IP_ADDRESS', '192.168.1.1')
        """

        from mage import client_id
        retval = cls.mutate('create_asset', input={'asset_type': asset_type, 'assetClientId': client_id, 'asset_source': 'CUSTOMER_DEFINED', 'asset_identifier': id, **kwargs})
        if retval:
            retval = cls.init(retval)
        return retval


    @property
    def credentials(self):
        """
        Associated credentials.

        Returns:
            `ListObject` of `CredentialConnection <credential_connection.CredentialConnection>`
        """
        from .credential_connection import CredentialConnection
        return self._nested_resource_list(CredentialConnection, 'credentials', CredentialConnection.__field_names__)


    @property
    def findings(self):
        """
        Associated findings.

        Returns:
            `ListObject` of `Finding <finding.Finding>`
        """
        from .finding import Finding
        return self._nested_resource_list(Finding, 'findings')


    @property
    def findings_filter(self):
        """
        Findings associated with this asset.

        Returns:
            `Filter`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> asset = mage.Asset.eq(asset_identifier='www.example.com')[0]
            >>> list(asset.findings().auto_paging_iter())
        """
        from .finding import Finding
        return Finding.eq(affected_asset_id=self.id)


    @classmethod
    def by_identifier(cls, asset_identifier = None, **params):
        Filter.normalize_list_filters(params)

        if asset_identifier:
            params['asset_identifier'] = asset_identifier

        if 'limit' in params:
            return cls._retrieve_all('assets_by_identifier', **params)
        else:
            return cls._retrieve('assets_by_identifier', **params)
