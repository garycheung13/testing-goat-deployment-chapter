from selenium import webdriver
import unittest

# functional tests subclass the TestCase class


class NewVisitorTest(unittest.TestCase):
    # special function inherited from unittest parent class
    # called before running tests
    def setUp(self):
        self.browser = webdriver.Firefox()

    # special function inherited from unittest parent class
    # called after running tests
    def tearDown(self):
        self.browser.quit()

    # methods starting with test will be ran by test runner
    def test_can_start_a_list_and_retrieve_it_later(self):
        # check out homepage
        self.browser.get('http://localhost:8000')
        # user notices the page title
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
