import json
import mage
import tempfile
import time
import unittest

class TestLead(unittest.TestCase):

    TEST_ASSET = "unittest.example.com"

    @classmethod
    def setUpClass(cls):
        mage.connect()
        cls.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        cls.ar_id = cls.a.start()
        cls.ar = mage.AssessmentRun.get(cls.ar_id)
        cls.lead = mage.Lead.create('Default Password on WEBSRV1', 'Password has not been changed yet.', cls.ar_id)
        # give time to replicate to ES
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.ar.stop()
        cls.a.delete()
        cls.lead.delete()

    def test_create(self):
        self.assertIsInstance(self.lead, mage.Lead)

    def test_assessment(self):
        self.assertRaises(NotImplementedError, lambda:self.lead.assessment)

    def test_assessment_run(self):
        self.assertIsInstance(self.lead.assessment_run, mage.AssessmentRun)
        self.assertEqual(self.lead.assessment_run.id, self.ar_id)

if __name__ == '__main__':
    unittest.main()
