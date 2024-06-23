import argparse
from spider import WebSpider
import time

def main():
    # Argument Parser
    parser = argparse.ArgumentParser(description="Web Spider with Selenium")
    parser.add_argument("base_url", help="Base URL of the website to scrape")
    parser.add_argument("continue_selector", help="CSS selector for the 'Continue' element")
    parser.add_argument("--print_info", action="store_true", help="Print information found")

    # Add a new argument to accept a list of tuples for query selectors and property names
    parser.add_argument("--query_selectors", nargs='+', metavar=('property_name', 'css_selector'),
                        help="List of tuples containing property names and corresponding CSS selectors")

    args = parser.parse_args()

    # Convert the list of tuples to a dictionary
    query_selectors = dict(zip(args.query_selectors[::2], args.query_selectors[1::2])) if args.query_selectors else {}

    # Begin the Spidering Application
    spider = WebSpider(args.base_url, query_selectors, args.continue_selector, args.print_info)
    
    # Parse page
    spider.parse_page(dev=True)

    input('waiting...')
    # Click element and recurse if needed
    spider.click_element_and_check_domain(args.continue_selector)
    
    time.sleep(1)
    print (spider)
    
    time.sleep(1)
    # Close Spider
    spider.close()

if __name__ == "__main__":
    main()
