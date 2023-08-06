import json
import mage
import tempfile
import time
import unittest

class TestAssetGroup(unittest.TestCase):

    TEST_ASSET = "unittest.example.com"

    @classmethod
    def setUpClass(cls):
        mage.connect()

    def setUp(self):
        self.a = None
        self.ag = mage.AssetGroup.create('UNITTEST')
        self.asset = None

    def tearDown(self):
        if self.a:
            self.a.delete()
        if self.ag:
            self.ag.delete()
        if self.asset:
            self.asset.delete()

    def test_assessments(self):
        self.assertIsInstance(self.ag.assessments, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ag.assessments.cls, mage.AssessmentAssetGroupConnection)

    def test_assets(self):
        self.assertIsInstance(self.ag.assets, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ag.assets.cls, mage.AssetGroupConnection)

    def test_connect_assessment(self):
        self.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        connection = self.ag.connect(self.a)
        self.assertIsInstance(connection, mage.AssessmentAssetGroupConnection)
        self.assertEqual(len(list(self.ag.assessments.auto_paging_iter())), 1)

    def test_connect_assessment_by_id(self):
        self.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        connection = self.ag.connect(assessment_id=self.a.id)
        self.assertIsInstance(connection, mage.AssessmentAssetGroupConnection)
        self.assertEqual(len(list(self.ag.assessments.auto_paging_iter())), 1)

    def test_connect_asset(self):
        self.asset = mage.Asset.create('DOMAIN', 'unittest.example.com')
        connection = self.ag.connect(self.asset)
        self.assertIsInstance(connection, mage.AssetGroupConnection)
        self.assertEqual(len(list(self.ag.assets.auto_paging_iter())), 1)

    def test_connect_asset_by_id(self):
        self.asset = mage.Asset.create('DOMAIN', 'unittest.example.com')
        connection = self.ag.connect(asset_id=self.asset.id)
        self.assertIsInstance(connection, mage.AssetGroupConnection)
        self.assertEqual(len(list(self.ag.assets.auto_paging_iter())), 1)

    def test_connect_bad_type(self):
        self.assertRaises(TypeError, self.ag.connect, self.ag)

    def test_create(self):
        self.assertIsInstance(self.ag, mage.AssetGroup)

if __name__ == '__main__':
    unittest.main()
