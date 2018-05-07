from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):
    # implicitly done when using test client
    # def test_root_url_resolves_to_homepage_view(self):
    #     found = resolve('/')
    #     # asserting that the homepage function matches the home_page function defined in views
    #     self.assertEqual(found.func, home_page)

    def test_homepage_returns_correct_html(self):
        # old test
        # request = HttpRequest() # dictionary containing the request's metadata
        # response = home_page(request) # pass into home_page view function to get a response object
        # html = response.content.decode('utf8') # decode response object
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.strip().endswith('</html>'))

        # using django test client
        response = self.client.get('/')
        # checking for template match instead of trying to render to string
        self.assertTemplateUsed(response, 'home.html')
