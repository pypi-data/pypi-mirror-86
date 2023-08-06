import datetime
import unittest
import os

from pds_doi_service.core.db.doi_database import DOIDataBase
from pds_doi_service.core.actions.check import DOICoreActionCheck

from pds_doi_service.core.util.general_util import get_logger

logger = get_logger(__name__)

class MyTestCase(unittest.TestCase):

    # As of 06/30/2020, OSTI has the below DOI records (['10.17189/21938','10.17189/21939','10.17189/21940']) in their test server so this test will work
    # to demonstrate that they have new status of 'Reserved'.  If for some reason the server has been wiped clean, this unit test will still run
    # but won't show any status changed.

    db_name = 'doi_temp.db'

    @classmethod
    def setUp(cls):
        logger.info("Creating test artifact database file {self.db_name}")
        _database_obj = DOIDataBase('doi_temp.db')

        lid = 'urn:nasa:pds:lab_shocked_feldspars'
        vid = '1.0'
        transaction_key = './transaction_history/img/2020-06-15T18:42:45.653317'
        transaction_date = datetime.datetime.now()
        status = 'Pending'
        title = 'Laboratory Shocked Feldspars Bundle'
        product_type = 'Collection'
        product_type_specific = 'PDS4 Collection'
        submitter = 'Qui.T.Chau@jpl.nasa.gov'
        discipline_node = 'img'

        # Write a record with new doi into temporary database.
        doi = '10.17189/21940'
        title = 'Laboratory Shocked Feldspars Bundle 1'
        lid = 'urn:nasa:pds:lab_shocked_feldspars1'
        logger.info("Writing doi metadata for {doi} to db_name {db_name}")
        _database_obj.write_doi_info_to_database(lid, vid, transaction_key, doi, transaction_date, status,
                                                 title, product_type, product_type_specific, submitter, discipline_node)

        # Write another record with new doi into temporary database.
        doi = '10.17189/21939'
        title = 'Laboratory Shocked Feldspars Bundle 2'
        lid = 'urn:nasa:pds:lab_shocked_feldspars2'
        logger.info("Writing doi metadata for {doi} to db_name {db_name}")
        _database_obj.write_doi_info_to_database(lid, vid, transaction_key, doi, transaction_date, status,
                                                 title, product_type, product_type_specific, submitter, discipline_node)

        # Write another record with new doi into temporary database.
        doi = '10.17189/21938'
        title = 'Laboratory Shocked Feldspars Bundle 3'
        lid = 'urn:nasa:pds:lab_shocked_feldspars3'
        discipline_node = 'naif'
        logger.info("Writing doi metadata for {doi} to db_name {db_name}")
        _database_obj.write_doi_info_to_database(lid, vid, transaction_key, doi, transaction_date, status,
                                                 title, product_type, product_type_specific, submitter, discipline_node)

        # Check for 'Pending' records
        cls._action = DOICoreActionCheck(cls.db_name)


    @classmethod
    def tearDown(cls):
        if os.path.isfile(cls.db_name):
            os.remove(cls.db_name)
            logger.info("Removed test artifact database file {self.db_name}")

    def test_1(self):
        # Note that if the status return 'Error', is OK depending on what the server has for the following 3 dois: ['10.17189/21938','10.17189/21939','10.17189/21940']
        logger.info("test making a query to database and update any status changed from 'Pending' to something else .  This test would only work if the authentication for OSTI has been set up.")
        # By default, the DOICoreActionCheck will query for status = 'Pending' in database record.  The parameter query_criterias is for query
        # criteria that are different than the default ones.
        # The parameter to_send_mail_flag is set to True by default if not specified.  We don't want to send out emails needlessly.
        # If desire to get the email, the parameter to_send_mail_flag can be set to True
        result_list = self._action.run(to_send_mail_flag=False) # Don't send email with this line.
        logger.info(result_list)




if __name__ == '__main__':
    unittest.main()
