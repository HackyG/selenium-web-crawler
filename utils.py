
from selenium import webdriver
import pprint
import re

class Utilities():
    def __init__(self, base_url, query_selectors, continue_selector, print_info=False):
        self.base_url = base_url
        self.query_selectors = query_selectors
        self.continue_selector = continue_selector
        self.print_info = print_info
        self.driver = self.init_driver()
        self.data = {}
        self.is_changed = False
        self.current_domain = self.base_url

    def __str__(self):
        dat = ''
        for key, value in self.data.items():
            dat += f'{key} : {len(value)} '
        return f'Spider Data:\n{pprint.pformat(self.data)}\n\nData Lengths: {dat}\nDomain Changed: {self.is_changed}'

    def propertyCheck(self, property, string, returnAdditionalInfo=False):
        if property in string:
            split_result = string.split(property)
            string = split_result[0]
            if returnAdditionalInfo:
                return split_result[1][1:]
            return True
        return False
    
    def strip_text_characters(self, input_string):
        # Use a regular expression to match and remove all text characters, symbols, and spaces
        stripped_string = re.sub(r'[a-zA-Z<>/£\-\s]', '', input_string)
        
        if stripped_string == '':
            return -1  # Assuming -1 for n/a
        else:
            try:
                return float(stripped_string)
            except ValueError:
                # Handle the case where the stripped string is not a valid float
                return -1  # Assuming -1 for n/a if conversion to float fails


     ## Init Web Driver
   
    def init_driver(self):
        print('initing')
        ## Driver Options
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_setting_values': {}}
        options.add_experimental_option('prefs', prefs)
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        ## Return Web Driver Instance
        return webdriver.Chrome(options=options)
    
    def set_element_background_color(self, element, color):
        self.driver.execute_script(f"arguments[0].style.backgroundColor = '{color}';", element)

    ## Close Driver
    def close(self):
        self.driver.quit()
