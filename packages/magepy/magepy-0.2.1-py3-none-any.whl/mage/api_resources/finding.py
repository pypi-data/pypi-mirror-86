from .abstract import *
from .. import schema

class Finding( ListableAPIResource, MutableAPIResource ):
    """
    Attributes:
        affected_asset_id (str): ID of the associated asset
        created_at (str): When the finding was created (e.g., '2020-01-02T03:04:56.789Z')
        description (str): A description of the finding
        evidence (mage.schema.AWSJSON): Evidence supporting the finding
        file_links (list of str):
        files (list of :class:`mage.schema.S3Object`):
        id (str): Unique finding ID
        references (list of str): List of references for additional information
        recommendations (list of str): List of recommendations
        risk (float): Risk associated with this finding
        severity (mage.schema.Severity): How severe the finding is
        title (str): The title of the finding
        updated_at (str): When the finding was last updated (e.g., '2020-01-02T03:04:56.789Z')
    """

    _SEARCH_FN = 'search_findings'
    _UPDATE_FN = 'update_finding'
    _DELETE_FN = 'delete_finding'

    __field_names__ = schema.Finding.__field_names__


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
    def assessment_id(self):
        """
        Warning:
            Not Implemented.  Use assessment_run_id instead.

        Todo:
            Rename assessment_id to assessment_run_id in the schema and remove this method.
        """
        raise NotImplementedError("Use 'assessment_run_id' instead of 'assessment_id'")


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
    def assessment_run_id(self):
        """
        ID of the associated assessment run.

        Returns:
            str

        Todo:
            Rename assessment_id to assessment_run_id in the schema and remove this method.
        """
        return self.assessment_id


    @property
    def affected_asset(self):
        """
        The associated asset.

        Returns:
            `Asset <asset.Asset>`
        """

        from .asset import Asset
        return self._nested_resource(Asset, 'affected_asset')


    @classmethod
    def create(cls, severity, title, description, assessment_run_id, asset_id, **kwargs):
        """
        Creates a finding for an assessment run.

        Args:
            severity (mage.schema.Severity):
            title (str):
            description (str):
            assessment_run_id (str):
            asset_id (str):
            **kwargs: Additional arguments to initialize the finding with

        Returns:
            `Finding <finding.Finding>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Finding.create('HIGH', 'Default Password', 'Password has not been changed yet.', '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222')
        """

        retval = cls.mutate('create_finding', input={'severity': severity, 'affectedAssetId': asset_id, 'description': description, 'title': title, 'assessmentId': assessment_run_id, **kwargs})
        if retval:
            retval = cls.init(retval)
        return retval
