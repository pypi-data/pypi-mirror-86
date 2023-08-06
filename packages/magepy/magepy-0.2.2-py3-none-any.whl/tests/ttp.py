import json
import mage
import tempfile
import time
import unittest

class TestTTP(unittest.TestCase):

    TEST_ASSET = "unittest.example.com"

    @classmethod
    def setUpClass(cls):
        mage.connect()
        cls.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        cls.ar_id = cls.a.start()
        cls.ar = mage.AssessmentRun.get(cls.ar_id)
        cls.asset = mage.Asset.create('DOMAIN', cls.TEST_ASSET)
        cls.ttp = mage.TTP.create('Port Scan', cls.ar_id, cls.asset.id)
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.ar.stop()
        cls.a.delete()
        cls.asset.delete()
        cls.ttp.delete()

    def test_create(self):
        self.assertIsInstance(self.ttp, mage.TTP)

    def test_assessment_run(self):
        self.assertIsInstance(self.ttp.assessment_run, mage.AssessmentRun)
        self.assertEqual(self.ttp.assessment_run.id, self.ar_id)

    def test_asset(self):
        self.assertIsInstance(self.ttp.asset, mage.Asset)
        self.assertEqual(self.ttp.asset.id, self.asset.id)

if __name__ == '__main__':
    unittest.main()
