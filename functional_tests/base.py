from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 10

# functional tests subclass the TestCase class


class FunctionalTest(StaticLiveServerTestCase):
    # special function inherited from unittest parent class
    # called before running tests
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    # special function inherited from unittest parent class
    # called after running tests
    def tearDown(self):
        self.browser.quit()

    # either finds the text content and test passes
    # or times out if not found
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()  # current time
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                # if time difference greater than max wait time,
                # throw the exception that prevented the test from passing
                # will tell us if it was because page didn't load (WebDriverException) or
                # because test actually failed (Assertion error)
                if (time.time() - start_time) > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time() # time at start of function call
        while True:
            try:
                return fn() # execute and return the result of the lambda fn
            except (AssertionError, WebDriverException) as e:
                if (time.time() - start_time) > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')