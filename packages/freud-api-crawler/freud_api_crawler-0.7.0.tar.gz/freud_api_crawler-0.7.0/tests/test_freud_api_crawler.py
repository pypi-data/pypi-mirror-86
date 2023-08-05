#!/usr/bin/env python

"""Tests for `freud_api_crawler` package."""

import os
import unittest
from click.testing import CliRunner

from freud_api_crawler import freud_api_crawler as frd
from freud_api_crawler import string_utils
from freud_api_crawler import cli


MANIFESTATION_ID = "a10e8c78-adad-4ca2-bfcb-b51bedcd7b58"
MANIFESTATION_PAGE_ID = "5126755a-eeae-4f53-82f9-aaa3a6fd81a9"
MANIFESTATION_PAGE_URL = "https://www.freud-edition.net/jsonapi/node/manifestation_\
seite/5126755a-eeae-4f53-82f9-aaa3a6fd81a9"


class TestFreud_api_crawler(unittest.TestCase):
    """Tests for `freud_api_crawler` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.frd_manifestion_obj = frd.FrdManifestation(MANIFESTATION_ID)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_not_authenticated(self):
        """Test if os-envs are set"""
        frd_obj = frd.FrdClient()
        if frd.FRD_PW and frd.FRD_PW:
            self.assertTrue(frd_obj.authenticated)
        else:
            self.assertFalse(frd_obj.authenticated)

    def test_001_endpoints_no_auth(self):
        """Test of endpoints-method"""
        frd_obj = frd.FrdClient(user=False, pw=False)
        endpoints = frd_obj.list_endpoints()
        self.assertFalse(endpoints)

    def test_002_endpoints_with_auth(self):
        """Test of endpoints-method"""
        frd_obj = frd.FrdClient()
        endpoints = frd_obj.list_endpoints()
        self.assertTrue(endpoints)
        self.assertTrue('node' in endpoints.keys())

    def test_003_endpoints_no_auth(self):
        """check if not authenticated condition works"""
        frd_obj = frd.FrdClient(user=False, pw=False)
        endpoints = frd_obj.list_endpoints()
        self.assertFalse(endpoints)

    def test_004_FrdManifestation_init_test(self):
        """check for correct id"""
        frd_obj = self.frd_manifestion_obj
        self.assertEqual(frd_obj.manifestation_id, MANIFESTATION_ID)

    def test_005_FrdManifestation_init_test(self):
        """test if correct manifestation endpoint is returned"""
        frd_obj = self.frd_manifestion_obj
        self.assertEqual(
            frd_obj.manifestation_endpoint,
            f'https://www.freud-edition.net/jsonapi/node/manifestation/{MANIFESTATION_ID}'
        )

    def test_006_FrdManifestation_return_manifestation(self):
        """check if correct manifestation is returned"""
        frd_obj = self.frd_manifestion_obj
        fetch_man_id = frd_obj.manifestation['data']['id']
        self.assertEqual(fetch_man_id, MANIFESTATION_ID)

    def test_007_FrdManifestation_page_count(self):
        """count related pages"""
        frd_obj = self.frd_manifestion_obj
        pages = frd_obj.page_count
        self.assertEqual(pages, 22)

    def test_008_FrdManifestation_number_of_metaattributes(self):
        """Count meta_attributes"""
        frd_obj = self.frd_manifestion_obj
        test_item = frd_obj.meta_attributes
        self.assertEqual(len(test_item), 52)

    def test_009_FrdManifestation_title(self):
        """Check title"""
        frd_obj = self.frd_manifestion_obj
        test_item = frd_obj.md__title
        self.assertEqual(test_item, 'II. Die infantile Sexualität')

    def test_010_FrdManifestation_page(self):
        """Check loading of manifestation_seite"""
        frd_obj = self.frd_manifestion_obj
        for x in [MANIFESTATION_PAGE_ID, MANIFESTATION_PAGE_URL]:
            page = frd_obj.get_page(page_id=x)
            test_item = page['data']['id']
            self.assertEqual(test_item, MANIFESTATION_PAGE_ID)

    def test_011_str_cleaning(self):
        """test clean_markup function"""
        frd_obj = self.frd_manifestion_obj
        page = frd_obj.get_page(page_id=MANIFESTATION_PAGE_ID)
        body = page['data']['attributes']['body']['processed']
        test_pattern = string_utils.CLEAN_UP_PATTERNS[0][0]
        cleaned_body = string_utils.clean_markup(body)
        self.assertTrue(test_pattern not in cleaned_body)

    def test_012_str_cleaning(self):
        """test clean_markup function"""
        frd_obj = self.frd_manifestion_obj
        page = frd_obj.get_page(page_id=MANIFESTATION_PAGE_ID)
        result = frd_obj.process_page(page)
        self.assertEqual(result['id'],  MANIFESTATION_PAGE_ID)
        self.assertTrue('body' in result.keys())

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'freud_api_crawler.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
