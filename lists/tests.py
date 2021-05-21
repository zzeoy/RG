
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item

class HomePageTest(TestCase):
    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    def test_root_url_resolve_to_home_page_view(self):
        found =resolve('/')
        self.assertEqual(found.func,home_page)
    def test_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')
    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def test_can_save_a_POST_request(self):
        item_text = 'A new list item'
        self.client.post('/', data={'item_text': item_text})

        # 检查是否把一个新Item对象存入数据库
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        # 检查文本是否正确
        self.assertEqual(new_item.text, item_text)

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
'''
    def test_can_save_a_POST_request(self):
        response=self.client.post('/',data={'item_text':'A new list item'})

        item_text = 'A new list item'
        # 检查是否把一个新Item对象存入数据库
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        # 检查文本是否正确
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/')
        '''
class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item_text = 'The first (ever) list item'
        first_item.text = first_item_text
        first_item.save()

        second_item = Item()
        second_item_text = 'Item the second'
        second_item.text = second_item_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        #self.assertEqual(first_saved_item.text, first_item_text)
        #self.assertEqual(second_saved_item.text, second_item_text)
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


# Create your tests here.
#class SmokeTest(TestCase):
 #   def test_bad_maths(self):
  #      self.assertEaual(1+1,3)
  
