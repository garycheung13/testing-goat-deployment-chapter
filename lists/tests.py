# django functions
from django.test import LiveServerTestCase
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

    # django flushes db between tests so this logic should always work
    def test_can_save_a_POST_request(self):
        # make a request using the test client
        response = self.client.post('/', data={'item_text': 'A new list item'})

        # We check that one new Item has been saved to the database.
        # objects.count() is a shorthand for objects.all().count()
        self.assertEqual(Item.objects.count(), 1)
        # objects.first() is the same as doing objects.all()[0]
        new_item = Item.objects.first()
        # Check that text is correct
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    # doesn't add new items on get requests to homepage
    def test_only_saves_item_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        # shorthand for adding fields and saving
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())


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
