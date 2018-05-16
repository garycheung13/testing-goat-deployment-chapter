from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase

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

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # methods starting with test will be ran by test runner
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
        time.sleep(1)

        # page refreshes so get the element again
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')
        self.fail('Finish the test!')
