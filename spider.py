from utils import Utilities
from selenium import webdriver
from selenium.webdriver.common.by import By

def Spider(Utilities):
    pass

    def continue_and_click():
        return

    def parse_page(self, dev=False):
        # Load the base URL in the browser
        self.load_page(self.base_url)

        # Dictionary to store scraped data
        data = {}

        # Display CSS Selectors being checked
        print('\n\tCSS Selectors:')

        # Loop through each CSS selector specified in query_selectors
        for key, param in self.query_selectors.items():
            # If in development mode, print information about the current selector
            if dev:
                print(f'Checking for {key} with {param}')

            # Check for special conditions in the selector
            if '?' in param:
                # Check if image, link, table, and parseDetails conditions are present
                img_pass = self.propertyCheck('?image', param)
                link_pass = self.propertyCheck('?link', param)
                table_pass = self.propertyCheck('?table', param)
                detail_pass = self.propertyCheck('?parseDetails', param, True)

            try:
                # Find elements based on the CSS selector
                elements = self.driver.find_elements(By.CSS_SELECTOR, param.split('?')[0] if '?' in param else param)
            except:
                # Handle the case where no elements are found for the selector
                print('Nothing found from Selectors')
                continue

            # List to store data for the current selector
            dataArr = []

            # Loop through each element found using the CSS selector
            for element in elements:
                # Set background color for the element (custom method)
                self.set_element_background_color(element, key)

                # Check if special conditions are present in the selector
                if '?' in param:
                    # Process different conditions based on the selector type
                    if img_pass:
                        try:
                            # Extract image URL from the element
                            img_url = element.get_attribute('srcset').split(',')[0].replace(' ', '') if element.get_attribute('srcset') != '' else element.get_attribute('src')
                            dataArr.append(img_url)
                        except:
                            dataArr.append('error img')
                        continue

                    if link_pass:
                        # Extract link URL from the element
                        dataArr.append(element.get_attribute('href'))
                        continue

                    if table_pass:
                        # Extract and format HTML table from the element
                        table_html = '<table>' + element.get_attribute('innerHTML') + '</table>'
                        dataArr.append(self.print_html_table_by_row(table_html))
                        continue

                    if detail_pass:
                        # Extract and parse details from the element
                        text_chunk_arr = element.text.split('\n')
                        details_chunk_arr = detail_pass.split(',')
                        found = [False] * len(details_chunk_arr)

                        # Loop through text chunks and details to match and extract information
                        for i, text_chunk in enumerate(text_chunk_arr):
                            for j, detail_chunk in enumerate(details_chunk_arr):
                                if text_chunk == detail_chunk and not found[j]:
                                    name = self.propertyMap[param + j]
                                    found[j] = True
                                    value_index = i + 1

                                    # Special handling for 'Servings' property
                                    if name == 'Servings':
                                        dataArr[name].append(int(self.strip_text_characters_int(text_chunk_arr[value_index])))
                                    else:
                                        dataArr[name].append(text_chunk_arr[value_index])

                                    break

                        break

                    # If no special conditions, append element text to dataArr
                    dataArr.append(element.text.replace('\n', ';'))

            # Remove empty items from dataArr
            filteredDataArr = [item for item in dataArr if item != ""]

            # Parse for Float if specified in the selector (typo early on :( )
            if '?parseInt' in param:
                for x in range(0, len(filteredDataArr)):
                    filteredDataArr[x] = self.strip_text_characters(filteredDataArr[x])

            # Store the data for the current selector in the data dictionary
            data[key] = filteredDataArr

        # Update the data attribute with the scraped data
        self.data = data
