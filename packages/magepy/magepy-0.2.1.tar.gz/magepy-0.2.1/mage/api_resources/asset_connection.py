from .abstract import *
from .. import schema

class AssetConnection( MutableAPIResource ):
    """
    A connection indicating how two assets are related to each other.

    Attributes:
        assessment_run_id (str): ID of the associated assessment run 
        asset_destination_id (str): ID of the destination asset
        asset_source_id (str): ID of the source asset
        created_at (str): When the connection was created (e.g., '2020-01-02T03:04:56.789Z')
        discovery_method (mage.schema.DiscoveryMethod): How the connection was discovered
        id (str): Unique connection ID
        state (mage.schema.AssetConnectionState): The state of the connection
        updated_at (str): When the connection was last updated (e.g., '2020-01-02T03:04:56.789Z')
    """

    _UPDATE_FN = 'update_asset_connection'
    _DELETE_FN = 'delete_asset_connection'

    __field_names__ = schema.AssetConnection.__field_names__


    @property
    def assessment(self):
        """
        Warning:
            Not Implemented.  Use assessment_run instead.

        Todo:
            Rename assessment to assessment_run in the schema and remove this method.
        """
        raise NotImplementedError("Call 'assessment_run' instead of 'assessment'")


    @property
    def assessment_run(self):
        """
        The associated assessment run.

        Returns:
            `AssessmentRun <assessment_run.AssessmentRun>`

        Todo:
            Rename assessment to assessment_run in the schema then update this method by renaming assessment to assessment_run.
        """
        from .assessment_run import AssessmentRun
        return self._nested_resource(AssessmentRun, 'assessment')


    @property
    def asset_source(self):
        """
        The associated source asset.

        Returns:
            `Asset <asset.Asset>`
        """
        from .asset import Asset
        return self._nested_resource(Asset, 'asset_source')


    @property
    def asset_destination(self):
        """
        The associated destination asset.

        Returns:
            `Asset <asset.Asset>`
        """
        from .asset import Asset
        return self._nested_resource(Asset, 'asset_destination')
