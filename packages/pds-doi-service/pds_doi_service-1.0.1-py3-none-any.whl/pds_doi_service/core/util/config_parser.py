#!/bin/python
#
#  Copyright 2020, by the California Institute of Technology.  ALL RIGHTS
#  RESERVED. United States Government Sponsorship acknowledged. Any commercial
#  use must be negotiated with the Office of Technology Transfer at the
#  California Institute of Technology.
#
#------------------------------

import os
from os.path import abspath, dirname, exists, join
import sys
from xml.etree import ElementTree
import configparser
from pds_doi_service.core.util.general_util import get_logger
from pds_doi_service.core.outputs.output_util import DOIOutputUtil

logger = get_logger(__name__)


class DOIConfigUtil:
    global m_debug_mode
    m_module_name = 'DOIConfigUtil:'
    m_debug_mode = False

    m_DOIOutputUtil = DOIOutputUtil()

    def get_config(self):
        parser = configparser.ConfigParser()
        candidates = ['conf.ini.default',
                      'conf.ini', ]
        # default configuration
        conf_default = 'conf.ini.default'
        conf_default_path = abspath(join(dirname(__file__), conf_default))
        conf_user = 'pds_doi_service.ini'
        conf_user_prod_path = os.path.join(sys.prefix, conf_user)
        conf_user_dev_path = abspath(join(dirname(__file__), os.pardir, os.pardir, os.pardir, conf_user))
        candidates_full_path = [conf_default_path, conf_user_prod_path, conf_user_dev_path]
        logger.info(f"search configuration files in {candidates_full_path}")
        found = parser.read(candidates_full_path)
        logger.info(f"used configuration following files {found}")
        return parser

    def get_config_file_metadata(self,i_filename):
    #------------------------------
    #------------------------------
        function_name = self.m_module_name + 'get_config_file_metadata:'

        if not exists(i_filename):
            print("exiting: configuration file not found - " + i_filename)
            sys.exit(1)

        else:
            #------------------------------
            # Read the metadata in the configuration file
            #------------------------------
            with open(i_filename, 'rt') as f:
                tree = ElementTree.parse(f)
                doc  = tree.getroot()

        #------------------------------
        # Get the number of options in the config file
        #   <options numOptions="12">
        #------------------------------
        numOptions = tree.getroot().attrib.get("numOptions")
        #print "numOptions = '" + numOptions + "'"

        #------------------------------
        # Populate the dictionary with the options
        #------------------------------
        dict_configList = {}
        dict_configList = dict((e.tag, e.text) for e in doc)

        if (int(numOptions) == len(dict_configList)):
            #print("dict_configList: found correct number of options in dictionary: '" + numOptions + "'")
            pass
        else:
            print("exiting: dict_configList -- number of options ('" + numOptions + "') doesn't match elements in dictionary: '" + str(len(dict_configList)) + "'")
            sys.exit(1)

    #      for eachElement in dict_configList:
    #         print "dict_configList." + eachElement + " == '" + dict_configList.get(eachElement) + "'"

        #------------------------------
        # Populate the dictionary with the fixed_attribute options
        #------------------------------
        e = doc.find("fixed_attributes")
        numOptions = e.attrib.get("numOptions")

        dict_fixedList = {}

        for e in doc.find('fixed_attributes'):
            dict_fixedList[e.tag] = e.text
        if (int(numOptions) == len(dict_fixedList)):
            #print("dict_fixedList: found correct number of options in dictionary: '" + numOptions + "'")
            pass
        else:
            print("exiting: dict_fixedList -- number of options ('" + numOptions + "') doesn't match elements in dictionary: '" + str(len(dict_fixedList)) + "'")
            sys.exit(1)

        return(dict_configList, dict_fixedList)
