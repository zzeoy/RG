from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest
MAX_WAIT=10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser=webdriver.Firefox()
        

    def tearDown(self):
        self.browser.quit()
 
    def test_can_start_a_for_one_user(self):
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
    def test_mutiple_user_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox =self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)               
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        edith_list_url=self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        
        self.browser.quit()
        self.browser=webdriver.Firefox()
        
        self.browser.find_element_by_tag_name('body').test
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)
        
        inputbox =self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)               
        self.wait_for_row_in_list_table('1: Buy milk')
        
        francis_list_url=self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)
        
        page_text=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Buy milk',page_text)
        
    def wait_for_row_in_list_table(self, row_text):
        """辅助方法:检查row.text"""
        start_time=time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError,WebDriverException) as e:
                if time.time()-start_time>MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        #self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)
        #She notices the page title and header mention to-do lists
        self.assertIn('To-Do',self.browser.title)
        header_text=self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        #She is invited to enter a to-do item straight away
        inputbox =self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
            
        inputbox.send_keys('Buy peacock feathers')
        # 回车键
        inputbox.send_keys(Keys.ENTER)               
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 表格中数据有变化时，页面会自动刷新，需要重新查找元素
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        self.fail('finish the test!')
#if __name__=='__main__':
#    unittest.main(warnings='ignore')

