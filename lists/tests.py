# django functions
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

# client code
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    # implicitly done when using test client
    # def test_root_url_resolves_to_homepage_view(self):
    #     found = resolve('/')
    #     # asserting that the homepage function matches the home_page function defined in views
    #     self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        # old test
        # request = HttpRequest() # dictionary containing the request's metadata
        # response = home_page(request) # pass into home_page view function to get a response object
        # html = response.content.decode('utf8') # decode response object
        # self.assertTrue(html.startswith('<html>'))
        # self.assertIn('<title>To-Do lists</title>', html)
        # self.assertTrue(html.strip().endswith('</html>'))

        # All of Django's TestCase classes contains a django client object in its properties
        response = self.client.get('/')
        # checking for template match instead of trying to check diffrent different marku[]
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first ever list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first ever list item')
        self.assertEqual(second_saved_item.text, 'Item the second')