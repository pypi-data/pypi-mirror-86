import json
import mage
import tempfile
import time
import unittest

class TestAsset(unittest.TestCase):

    TEST_ASSET = "unittest.example.com"

    @classmethod
    def setUpClass(cls):
        mage.connect()

    def setUp(self):
        self.a = None
        self.ag = None
        self.asset = mage.Asset.create('DOMAIN', 'unittest.example.com')

    def tearDown(self):
        if self.a:
            self.a.delete()
        if self.ag:
            self.ag.delete()
        if self.asset:
            self.asset.delete()

    def test_connect_assessment(self):
        self.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        connection = self.asset.connect(self.a)
        self.assertIsInstance(connection, mage.AssessmentAssetConnection)
        self.assertEqual(len(list(self.asset.assessments.auto_paging_iter())), 1)

    def test_connect_assessment_by_id(self):
        self.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        connection = self.asset.connect(assessment_id=self.a.id)
        self.assertIsInstance(connection, mage.AssessmentAssetConnection)
        self.assertEqual(len(list(self.asset.assessments.auto_paging_iter())), 1)

    def test_connect_asset_group(self):
        self.ag = mage.AssetGroup.create('UNITTESTGROUP')
        connection = self.asset.connect(self.ag)
        self.assertIsInstance(connection, mage.AssetGroupConnection)
        self.assertEqual(len(list(self.asset.asset_groups.auto_paging_iter())), 1)

    def test_connect_asset_group_by_id(self):
        self.ag = mage.AssetGroup.create('UNITTESTGROUP')
        connection = self.asset.connect(asset_group_id=self.ag.id)
        self.assertIsInstance(connection, mage.AssetGroupConnection)
        self.assertEqual(len(list(self.asset.asset_groups.auto_paging_iter())), 1)

    def test_connect_bad_type(self):
        self.assertRaises(TypeError, self.asset.connect, 1)

    def test_connections(self):
        self.assertIsInstance(self.asset.connections, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.asset.connections.cls, mage.AssetConnection)

    def test_create(self):
        self.assertIsInstance(self.asset, mage.Asset)

    def test_credentials(self):
        self.assertIsInstance(self.asset.credentials, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.asset.credentials.cls, mage.CredentialConnection)

    def test_filters(self):
        self.assertIsInstance(self.asset.findings_filter, mage.Filter)
        self.assertEqual(self.asset.findings_filter._cls, mage.Finding)

    def test_findings(self):
        self.assertIsInstance(self.asset.findings, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.asset.findings.cls, mage.Finding)

if __name__ == '__main__':
    unittest.main()
