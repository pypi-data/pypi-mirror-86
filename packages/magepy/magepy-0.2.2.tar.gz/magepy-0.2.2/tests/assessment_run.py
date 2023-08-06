import json
import mage
import tempfile
import time
import unittest

class TestAssessmentRun(unittest.TestCase):

    TEST_ASSET = "unittest.example.com"

    @classmethod
    def setUpClass(cls):
        mage.connect()
        cls.a = mage.Assessment.create('EXTERNAL', name='UNITTEST')
        cls.ar_id = cls.a.start()
        cls.ar = mage.AssessmentRun.get(cls.ar_id)

    @classmethod
    def tearDownClass(cls):
        cls.ar.stop()
        cls.a.delete()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_assessment(self):
        self.assertIsInstance(self.ar.assessment, mage.Assessment)
        self.assertEqual(self.ar.assessment.id, self.a.id)

    def test_connections(self):
        self.assertIsInstance(self.ar.connections, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ar.connections.cls, mage.AssetConnection)

    def test_credentials(self):
        self.assertIsInstance(self.ar.credentials, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ar.credentials.cls, mage.AssessmentRunCredentialConnection)

    def test_discovered_assets(self):
        self.assertIsInstance(self.ar.discovered_assets, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ar.discovered_assets.cls, mage.AssessmentRunAssetConnection)

    def test_email_report_bad_type(self):
        self.assertRaises(TypeError, self.ar.email_report, 1)

    def test_email_report_blank_email_str(self):
        self.assertFalse(self.ar.email_report(''))

    def test_email_report_blank_email_array_str(self):
        self.assertFalse(self.ar.email_report(['']))

    def test_email_report_no_email(self):
        self.assertRaises(ValueError, self.ar.email_report)

    def test_filters(self):
        self.assertIsInstance(self.ar.findings_filter, mage.Filter)
        self.assertEqual(self.ar.findings_filter._cls, mage.Finding)
        self.assertIsInstance(self.ar.leads_filter, mage.Filter)
        self.assertEqual(self.ar.leads_filter._cls, mage.Lead)
        self.assertIsInstance(self.ar.ttps_filter, mage.Filter)
        self.assertEqual(self.ar.ttps_filter._cls, mage.TTP)

    def test_findings(self):
        self.assertIsInstance(self.ar.findings, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ar.findings.cls, mage.Finding)

    def test_leads(self):
        self.assertIsInstance(self.ar.leads, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ar.leads.cls, mage.Lead)

    #def test_get_report_url(self):
        #self.assertIsInstance(self.ar.get_report_url(), str)

    #def test_get_zip_url(self):
        #self.ar.get_zip_url()

    #def test_report_url(self):
        #self.assertIsInstance(self.ar.report_url, str)

    def test_stop(self):
        self.assertTrue(self.ar.stop())

    def test_ttps(self):
        self.assertIsInstance(self.ar.ttps, mage.api_resources.abstract.listable_api_resource.ListObject)
        self.assertEqual(self.ar.ttps.cls, mage.TTP)

if __name__ == '__main__':
    unittest.main()
