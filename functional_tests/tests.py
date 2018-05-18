from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from django.test import LiveServerTestCase

MAX_WAIT = 10

# functional tests subclass the TestCase class


class NewVisitorTest(LiveServerTestCase):
    # special function inherited from unittest parent class
    # called before running tests
    def setUp(self):
        self.browser = webdriver.Firefox()

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

    # methods starting with test will be ran by test runner
    # tests if home page has the proper content
    def test_can_start_a_list_and_retrieve_it_later(self):
        # check out homepage
        # django live server test parent class gives us this property
        self.browser.get(self.live_server_url)
        # user notices the page title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # add a todo item
        inputbox = self.browser.find_element_by_id('id_new_item')

        # placeholder text matches
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # add peacock feathers to todo list
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # page refreshes so get the element again
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Start a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # new user comes along

        # removing old session
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # creating a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets his own url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # make sure there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)