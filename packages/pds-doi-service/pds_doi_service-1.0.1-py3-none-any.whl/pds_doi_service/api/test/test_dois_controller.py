# coding: utf-8

from __future__ import absolute_import

from datetime import datetime
import json
import os
from os.path import abspath, dirname, exists, join
from unittest.mock import patch

import pds_doi_service.api.controllers.dois_controller
from pds_doi_service.api.encoder import JSONEncoder
from pds_doi_service.api.models import (DoiRecord, DoiSummary,
                                        LabelsPayload, LabelPayload)
from pds_doi_service.api.test import BaseTestCase


class TestDoisController(BaseTestCase):
    """DoisController integration test stubs"""
    # This attribute is defined at class level so it may be accessed
    # by patched methods
    test_data_dir = None

    @classmethod
    def setUpClass(cls):
        cls.test_dir = abspath(dirname(__file__))
        cls.test_data_dir = join(cls.test_dir, 'data')

        # Path to a temporary database to re-instantiate for every test
        cls.temp_db = join(cls.test_data_dir, 'temp.db')

    def setUp(self):
        # Set testing mode to True so endpoints know to look for a custom
        # database instance to work with
        self.app.config['TESTING'] = True

    def tearDown(self):
        # Remove the temp DB so a new one is created before each test
        if exists(self.temp_db):
            os.unlink(self.temp_db)

    def test_get_dois(self):
        """Test case for get_dois"""
        # For these tests, use a pre-existing database with some canned
        # entries to query for
        test_db = join(self.test_data_dir, 'test.db')

        # Start with a empty query to fetch all available records
        query_string = [('db_name', test_db)]

        response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                    method='GET',
                                    query_string=query_string)

        self.assert200(
            response,
            'Response body is : ' + response.data.decode('utf-8')
        )

        records = response.json

        # Test database should contain 2 records (matching those that are
        # submitted in test_post_dois)
        self.assertEqual(len(records), 2)

        # Now use a query string to ensure we can get specific records back
        query_string = [('node', 'eng'),
                        ('db_name', test_db)]

        response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                    method='GET',
                                    query_string=query_string)

        self.assert200(
            response,
            'Response body is : ' + response.data.decode('utf-8')
        )

        # Should only get one of the records back
        records = response.json
        self.assertEqual(len(records), 1)

        # Reformat JSON result into a DoiSummary object so we can check fields
        summary = DoiSummary.from_dict(records[0])

        self.assertEqual(summary.submitter, 'eng-submitter@jpl.nasa.gov')
        self.assertEqual(summary.lidvid, 'urn:nasa:pds:insight_cameras::1.1')
        self.assertEqual(summary.status, 'Draft')

    def draft_action_run_patch(self, **kwargs):
        """
        Patch for DOICoreActionDraft.run()

        Returns body of an OSTI XML label corresponding to a successful draft
        request.
        """
        draft_record_file = join(
            TestDoisController.test_data_dir, 'draft_osti_record.xml')
        with open(draft_record_file, 'r') as infile:
            return infile.read()

    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionDraft,
        'run', draft_action_run_patch)
    def test_post_dois_draft_w_url(self):
        """Test a draft POST with url input"""
        # We can use a file system path since were working with a local server
        input_bundle = join(self.test_data_dir, 'bundle_in.xml')

        # Start by submitting a draft request
        query_string = [('action', 'draft'),
                        ('submitter', 'eng-submitter@jpl.nasa.gov'),
                        ('node', 'eng'),
                        ('url', input_bundle),
                        ('db_name', self.temp_db)]

        draft_response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                          method='POST',
                                          query_string=query_string)

        self.assert200(
            draft_response,
            'Response body is : ' + draft_response.data.decode('utf-8')
        )

        # Recreate a DoiRecord from the response JSON and examine the
        # fields
        draft_record = DoiRecord.from_dict(draft_response.json[0])

        self.assertEqual(draft_record.submitter, 'eng-submitter@jpl.nasa.gov')
        self.assertEqual(draft_record.lidvid, 'urn:nasa:pds:insight_cameras::1.1')
        # Note we get Pending back from the parsed label, however
        # the object sent to transaction database has 'Draft' status
        self.assertEqual(draft_record.status, 'Pending')

    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionDraft,
        'run', draft_action_run_patch)
    def test_post_dois_draft_w_payload(self):
        """Test a draft POST with requestBody input"""
        input_bundle = join(self.test_data_dir, 'bundle_in.xml')

        with open(input_bundle, 'rb') as infile:
            body = infile.read()

        query_string = [('action', 'draft'),
                        ('submitter', 'eng-submitter@jpl.nasa.gov'),
                        ('node', 'eng'),
                        ('db_name', self.temp_db)]

        draft_response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                          method='POST',
                                          data=body,
                                          content_type='application/xml',
                                          query_string=query_string)

        self.assert200(
            draft_response,
            'Response body is : ' + draft_response.data.decode('utf-8')
        )

        # Recreate a DoiRecord from the response JSON and examine the
        # fields
        draft_record = DoiRecord.from_dict(draft_response.json[0])

        self.assertEqual(draft_record.submitter, 'eng-submitter@jpl.nasa.gov')
        self.assertEqual(draft_record.lidvid, 'urn:nasa:pds:insight_cameras::1.1')
        # Note we get Pending back from the parsed label, however
        # the object sent to transaction database has 'Draft' status
        self.assertEqual(draft_record.status, 'Pending')

    def reserve_action_run_patch(self, **kwargs):
        """
        Patch for DOICoreActionReserve.run()

        Returns body of an OSTI XML label corresponding to a successful reserve
        (dry-run) request.
        """
        draft_record_file = join(
            TestDoisController.test_data_dir, 'reserve_osti_record.xml')
        with open(draft_record_file, 'r') as infile:
            return infile.read()

    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionReserve,
        'run', reserve_action_run_patch)
    def test_post_dois_reserve(self):
        """Test dry-run reserve POST"""
        # Submit a new bundle in reserve (not submitted) status
        body = LabelsPayload(
            [LabelPayload(status='Reserved',
                          title='Laboratory Shocked Feldspars Bundle',
                          publication_date=datetime.now(),
                          product_type_specific='PDS4 Bundle',
                          author_last_name='Johnson',
                          author_first_name='J. R.',
                          related_resource='urn:nasa:pds:lab_shocked_feldspars')]
        )

        query_string = [('action', 'reserve'),
                        ('submitter', 'img-submitter@jpl.nasa.gov'),
                        ('node', 'img'),
                        ('db_name', self.temp_db)]

        reserve_response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                            method='POST',
                                            data=JSONEncoder().encode(body),
                                            content_type='application/json',
                                            query_string=query_string)

        self.assert200(
            reserve_response,
            'Response body is : ' + reserve_response.data.decode('utf-8')
        )

        # Recreate a DoiRecord from the response JSON and examine the
        # fields
        reserve_record = DoiRecord.from_dict(reserve_response.json[0])

        self.assertEqual(reserve_record.submitter, 'img-submitter@jpl.nasa.gov')
        self.assertEqual(reserve_record.lidvid, 'urn:nasa:pds:lab_shocked_feldspars')
        self.assertEqual(reserve_record.status, 'reserved_not_submitted')

    def test_post_dois_invalid_requests(self):
        """Test invalid POST requests"""

        # Test with an unknown action, should get Invalid Argument
        query_string = [('action', 'unknown'),
                        ('submitter', 'img-submitter@jpl.nasa.gov'),
                        ('node', 'img'),
                        ('db_name', self.temp_db)]

        error_response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                          method='POST',
                                          query_string=query_string)

        self.assert400(
            error_response,
            'Response body is : ' + error_response.data.decode('utf-8')
        )

        # Test draft action with no url or requestBody input
        query_string = [('action', 'draft'),
                        ('submitter', 'img-submitter@jpl.nasa.gov'),
                        ('node', 'img'),
                        ('db_name', self.temp_db)]

        error_response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                          method='POST',
                                          query_string=query_string)

        self.assert400(
            error_response,
            'Response body is : ' + error_response.data.decode('utf-8')
        )

        # Test reserve action with a url instead of a requestBody
        input_bundle = join(self.test_data_dir, 'bundle_in.xml')

        query_string = [('action', 'reserve'),
                        ('submitter', 'eng-submitter@jpl.nasa.gov'),
                        ('node', 'eng'),
                        ('url', input_bundle),
                        ('db_name', self.temp_db)]

        error_response = self.client.open('/PDS_APIs/pds_doi_api/0.1/dois',
                                          method='POST',
                                          query_string=query_string)

        self.assert400(
            error_response,
            'Response body is : ' + error_response.data.decode('utf-8')
        )

    def list_action_run_patch(self, **kwargs):
        """
        Patch for DOICoreActionList.run()

        Returns a JSON string corresponding to a successful search.
        The transaction_key is modified to point to the local test data
        directory.
        """
        return json.dumps(
            [
                {"status": "Draft", "update_date": 1603227852.560568,
                 "submitter": "eng-submitter@jpl.nasa.gov",
                 "title": "InSight Cameras Bundle 1.1", "type": "Dataset",
                 "subtype": "PDS4 Refereed Data Bundle", "node_id": "eng",
                 "lid": "urn:nasa:pds:insight_cameras", "vid": "1.1",
                 "doi": None, "release_date": None,
                 "transaction_key": TestDoisController.test_data_dir,
                 "is_latest": 1}
            ]
        )

    def release_action_run_patch(self, **kwargs):
        """
        Patch for DOICoreActionRelease.run()

        Returns body of an OSTI XML label corresponding to a successful release
        request.
        """
        draft_record_file = join(
            TestDoisController.test_data_dir, 'release_osti_record.xml')
        with open(draft_record_file, 'r') as infile:
            return infile.read()

    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionRelease,
        'run', release_action_run_patch)
    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionList,
        'run', list_action_run_patch)
    def test_post_release(self):
        """Test the release endpoint"""
        query_string = [('force', False),
                        ('db_name', self.temp_db)]

        release_response = self.client.open(
            '/PDS_APIs/pds_doi_api/0.1/dois/{lidvid}/release'
            .format(lidvid='urn:nasa:pds:insight_cameras::1.1'),
            method='POST',
            query_string=query_string
        )

        self.assert200(
            release_response,
            'Response body is : ' + release_response.data.decode('utf-8')
        )

        # Recreate a DoiRecord from the response JSON and examine the
        # fields
        release_record = DoiRecord.from_dict(release_response.json[0])

        self.assertEqual(release_record.submitter, 'eng-submitter@jpl.nasa.gov')
        self.assertEqual(release_record.lidvid, 'urn:nasa:pds:insight_cameras::1.1')
        self.assertEqual(release_record.status, 'Released')
        self.assertEqual(release_record.doi, '10.17189/21734')

        # Record field should match what we provided via patch method
        self.assertEqual(release_record.record, self.release_action_run_patch())

    def release_action_run_w_error_patch(self, **kwargs):
        """
        Patch for DOICoreActionRelease.run()

        Returns body of an OSTI XML label corresponding to errors returned
        from OSTI.
        """
        draft_record_file = join(
            TestDoisController.test_data_dir, 'error_osti_record.xml')
        with open(draft_record_file, 'r') as infile:
            return infile.read()

    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionRelease,
        'run', release_action_run_w_error_patch)
    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionList,
        'run', list_action_run_patch)
    def test_post_release_w_errors(self):
        """
        Test the release endpoint where errors are received back from the
        release action.
        """
        query_string = [('force', False),
                        ('db_name', self.temp_db)]

        error_response = self.client.open(
            '/PDS_APIs/pds_doi_api/0.1/dois/{lidvid}/release'
            .format(lidvid='urn:nasa:pds:insight_cameras::1.1'),
            method='POST',
            query_string=query_string
        )

        self.assert400(
            error_response,
            'Response body is : ' + error_response.data.decode('utf-8')
        )

        # Check the error response and make sure it contains all the errors
        # provided from the original XML
        errors = error_response.json['errors']

        self.assertEqual(errors[0]['name'], 'WarningDOIException')
        self.assertIn('Title is required', errors[0]['message'])
        self.assertIn('A publication date is required', errors[0]['message'])
        self.assertIn('A site URL is required', errors[0]['message'])
        self.assertIn('A product type is required', errors[0]['message'])
        self.assertIn('A specific product type is required for non-dataset types',
                      errors[0]['message'])

    def list_action_run_patch_missing(self, **kwargs):
        """
        Patch for DOICoreActionList.run()

        Returns a result corresponding to an unsuccessful search.
        """
        return '[]'

    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionList,
        'run', list_action_run_patch_missing)
    def test_post_release_missing_lid(self):
        """
        Test the release endpoint where no existing entry for the requested
        LID exists.
        """
        query_string = [('force', False),
                        ('db_name', self.temp_db)]

        error_response = self.client.open(
            '/PDS_APIs/pds_doi_api/0.1/dois/{lidvid}/release'
            .format(lidvid='urn:nasa:pds:insight_cameras::1.1'),
            method='POST',
            query_string=query_string
        )

        self.assert404(
            error_response,
            'Response body is : ' + error_response.data.decode('utf-8')
        )

        # Check the error response and make sure it contains the expected
        # error message
        errors = error_response.json['errors']

        self.assertEqual(errors[0]['name'], 'UnknownLIDVIDException')
        self.assertIn(
            'No record(s) could be found for LIDVID '
            'urn:nasa:pds:insight_cameras::1.1',
            errors[0]['message']
        )

    def list_action_run_patch_no_transaction_history(self, **kwargs):
        """
        Patch for DOICoreActionList.run()

        Returns a result corresponding to an entry where the listed
        transaction_key location no longer exists.
        """
        return json.dumps(
            [
                {"transaction_key": '/dev/null', "is_latest": 1}
            ]
        )

    @patch.object(
        pds_doi_service.api.controllers.dois_controller.DOICoreActionList,
        'run', list_action_run_patch_no_transaction_history)
    def test_post_release_missing_transaction_history(self):
        """
        Test the release endpoint where the requested LID returns an entry
        with a missing transaction_key location.
        """
        query_string = [('force', False),
                        ('db_name', self.temp_db)]

        error_response = self.client.open(
            '/PDS_APIs/pds_doi_api/0.1/dois/{lidvid}/release'
            .format(lidvid='urn:nasa:pds:insight_cameras::1.1'),
            method='POST',
            query_string=query_string
        )

        self.assert404(
            error_response,
            'Response body is : ' + error_response.data.decode('utf-8')
        )

        # Check the error response and make sure it contains the expected
        # error message
        errors = error_response.json['errors']

        self.assertEqual(errors[0]['name'], 'NoTransactionHistoryForLIDVIDException')
        self.assertIn(
            'Could not find an OSTI Label associated with LIDVID '
            'urn:nasa:pds:insight_cameras::1.1',
            errors[0]['message']
        )

    def test_get_doi_from_id(self):
        """Test case for get_doi_from_id"""
        response = self.client.open(
            '/PDS_APIs/pds_doi_api/0.1/dois/{doi_prefix}/{doi_suffix}'
            .format(doi_prefix='doi_prefix_example', doi_suffix='doi_suffix_example'),
            method='GET'
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_doi_from_id(self):
        """Test case for put_doi_from_id"""
        query_string = [('submitter', 'submitter_example'),
                        ('node', 'node_example'),
                        ('url', 'url_example')]
        response = self.client.open(
            '/PDS_APIs/pds_doi_api/0.1/dois/{doi_prefix}/{doi_suffix}'
            .format(doi_prefix='doi_prefix_example', doi_suffix='doi_suffix_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
