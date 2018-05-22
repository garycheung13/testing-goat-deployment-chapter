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
        new_list = List.objects.first() # list was created when page posted to lists/new
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create() # creating a list object with no fields
        # shorthand for adding fields and saving
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        # create a second list to assert that items are not on it
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        # create this to prevent using List.objects.first as shortcut during implementation
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')