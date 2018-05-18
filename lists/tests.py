# django functions
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

# client code
from lists.models import Item, List


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

class NewListTest(TestCase):
    # django flushes db between tests so this logic should always work
    def test_can_save_a_POST_request(self):
        # make a request using the test client
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        # We check that one new Item has been saved to the database.
        # objects.count() is a shorthand for objects.all().count()
        self.assertEqual(Item.objects.count(), 1)
        # objects.first() is the same as doing objects.all()[0]
        new_item = Item.objects.first()
        # Check that text is correct
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


class ListViewTest(TestCase):
    def test_displays_all_list_items(self):
        list_ = List.objects.create() # creating a list object with no fields
        # shorthand for adding fields and saving
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


class ListandItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first ever list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        # asserting the text and lists match
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first ever list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
