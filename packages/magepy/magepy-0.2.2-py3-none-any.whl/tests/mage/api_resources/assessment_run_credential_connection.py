from .abstract import *
from .. import schema

class AssessmentRunCredentialConnection( MutableAPIResource ):
    """
    Connection between an assessment run and a credential.

    Attributes:
        id (str): Unique connection ID
        created_at (str): When the connection was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the connection was last updated (e.g., '2020-01-02T03:04:56.789Z')
        asset_id (str): ID of the associated asset
        credential_id (str): ID of the associated credential
        link_type (mage.schema.CredentialLinkType):
    """

    _UPDATE_FN = 'update_assessment_run_credential_connection'
    _DELETE_FN = 'delete_assessment_run_credential_connection'

    __field_names__ = schema.AssessmentRunCredentialConnection.__field_names__


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
    def asset(self):
        """
        The associated asset.

        Returns:
            `Asset <asset.Asset>`
        """
        from .asset import Asset
        return self._nested_resource(Asset, 'asset')


    @classmethod
    def create(cls, assessment_run_id, credential_id):
        """
        Connects a credential to an assessment run.

        Args:
            assessment_run_id (str): ID of the assessment run
            credential_id (str): ID of the credential

        Returns:
            `AssessmentRunAssetConnection <assessment_run_asset_connection.AssessmentRunAssetConnection>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRunAssetConnection.create('11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222')
        """
        retval = cls.mutate('create_assessment_run_credential_connection', input={'credential_id': credential_id, 'assessment_run_id': assessment_run_id})
        if retval:
            retval = cls.init(retval)
        return retval


    @property
    def credential(self):
        """
        The associated credential.

        Returns:
            `Credential <credential.Credential>`
        """
        from .credential import Credential
        return self._nested_resource(Credential, 'credential')
