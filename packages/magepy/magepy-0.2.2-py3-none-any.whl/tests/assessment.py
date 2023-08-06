import json
import mage
import tempfile
import time
import unittest

class TestAssessment(unittest.TestCase):

    TEST_ASSET = "unittest.example.com"

    @classmethod
    def setUpClass(cls):
        mage.connect()

    def setUp(self):
        self.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        self.ar_id = None
        self.used_asset = False
        self.used_credential = False
        self.ag = None

    def tearDown(self):
        if self.ar_id:
            mage.AssessmentRun.stop(assessment_run_id=self.ar_id)
        if self.a:
            self.a.delete()
        if self.used_asset:
            for asset in mage.Asset.by_identifier(self.TEST_ASSET).auto_paging_iter():
                asset.delete()
        if self.ag:
            self.ag.delete()

    def test_create_assessment(self):
        self.assertIsInstance(self.a,mage.Assessment)

    def test_find_assessment_by_id(self):
        #BUG: created items are not always immediately findable
        time.sleep(2)
        result = mage.Assessment.eq(id=self.a.id).limit(1).search()
        self.assertEqual(len(result),1)

    def test_find_assessment_by_name(self):
        #BUG: created items are not always immediately findable
        time.sleep(2)
        result = mage.Assessment.eq(name=self.a.name).limit(1).search()
        self.assertEqual(len(result),1)

    def test_list_assessment(self):
        #BUG: created items are not always immediately findable
        time.sleep(2)
        result = mage.Assessment.list()
        self.assertTrue(len(result) > 0)

    def test_update_assessment_by_assignment(self):
        self.a.name = "KILROY"
        self.assertEqual(self.a.name, 'KILROY')

    def test_update_assessment_by_call(self):
        self.a.update(name="KILROY")
        self.assertEqual(self.a.name, 'KILROY')

    def test_start_assessment(self):
        self.ar_id = self.a.start()
        self.assertIsNotNone(self.ar_id)

    def test_load_assets(self):
        self.used_asset = True
        data = {'domains': [self.TEST_ASSET]}
        self.a.load_assets(data)
        self.assertEqual(len(self.a.assets), 1)

    def test_load_assets_bad_key(self):
        self.used_asset = True
        data = {'invalid':127}
        self.assertRaises(KeyError, self.a.load_assets, data)

    def test_load_assets_bad_type(self):
        self.used_asset = True
        data = {'ips':127}
        self.assertRaises(TypeError, self.a.load_assets, data)

    def test_load_assets_credential(self):
        self.used_credential = True
        data = {'cloud_credentials': [{'cloud_platform': 'AWS', 'access_key': '123'}]}
        self.a.load_assets(data)
        self.assertEqual(len(list(self.a.cloud_credentials.auto_paging_iter())), 1)

    def test_load_assets_from_filename(self):
        self.used_asset = True
        data = {'domains': self.TEST_ASSET}
        with tempfile.NamedTemporaryFile(mode='w+') as temp:
            temp.write(json.dumps(data))
            temp.flush()
            self.a.load_assets(temp.name)
        self.assertEqual(len(self.a.assets), 1)

    def test_load_assets_from_fileobj(self):
        self.used_asset = True
        data = {'domains': self.TEST_ASSET}
        with tempfile.TemporaryFile(mode='w+') as temp:
            temp.write(json.dumps(data))
            temp.flush()
            temp.seek(0)
            self.a.load_assets(temp)
        self.assertEqual(len(self.a.assets), 1)

    def test_load_assets_multiple(self):
        self.used_asset = True
        self.test_load_assets()
        self.test_load_assets()

    def test_load_assets_str(self):
        self.used_asset = True
        data = {'domains': self.TEST_ASSET}
        self.a.load_assets(data)
        self.assertEqual(len(self.a.assets), 1)

    def test_delete_assessment(self):
        self.assertIsNotNone(self.a.delete())
        self.a = None

    def test_list_runs(self):
        self.a.runs

    def test_create_schedule(self):
        self.assertTrue(self.a.create_schedule('DAILY', {'hour':'23', 'minute':'55'}))
        self.assertTrue(self.a.schedule)
        self.assertEqual(self.a.schedule.frequency, 'DAILY')
        self.assertEqual(self.a.schedule.time_expression.hour, '23')
        self.assertEqual(self.a.schedule.time_expression.minute, '55')

    def test_delete_schedule(self):
        self.test_create_schedule()
        self.assertTrue(self.a.delete_schedule())
        self.assertFalse(self.a.schedule)

    def test_filters(self):
        self.assertIsInstance(self.a.runs_filter, mage.Filter)
        self.assertEqual(self.a.runs_filter._cls, mage.AssessmentRun)
        self.assertIsInstance(self.a.asset_groups_filter, mage.Filter)
        self.assertEqual(self.a.asset_groups_filter._cls, mage.AssetGroup)
        self.assertIsInstance(self.a.cloud_credentials_filter, mage.Filter)
        self.assertEqual(self.a.cloud_credentials_filter._cls, mage.CloudCredential)

    def test_connect_asset(self):
        self.used_asset = True
        self.asset = mage.Asset.create('DOMAIN', self.TEST_ASSET)
        connection = self.a.connect(self.asset)
        self.assertIsInstance(connection, mage.AssessmentAssetConnection)
        self.assertEqual(len(list(self.a.assets.auto_paging_iter())), 1)

    def test_connect_asset_by_id(self):
        self.used_asset = True
        self.asset = mage.Asset.create('DOMAIN', self.TEST_ASSET)
        connection = self.a.connect(asset_id=self.asset.id)
        self.assertIsInstance(connection, mage.AssessmentAssetConnection)
        self.assertEqual(len(list(self.a.assets.auto_paging_iter())), 1)

    def test_connect_asset_group(self):
        self.ag = mage.AssetGroup.create('UNITTESTGROUP')
        connection = self.a.connect(self.ag)
        self.assertIsInstance(connection, mage.AssessmentAssetGroupConnection)
        self.assertEqual(len(list(self.a.asset_groups.auto_paging_iter())), 1)

    def test_connect_asset_group_by_id(self):
        self.ag = mage.AssetGroup.create('UNITTESTGROUP')
        connection = self.a.connect(asset_group_id=self.ag.id)
        self.assertIsInstance(connection, mage.AssessmentAssetGroupConnection)
        self.assertEqual(len(list(self.a.asset_groups.auto_paging_iter())), 1)

    def test_connect_bad_type(self):
        self.assertRaises(TypeError, self.a.connect, self.a)

if __name__ == '__main__':
    unittest.main()
