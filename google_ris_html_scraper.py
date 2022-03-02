# this script deploys a reverse image search on google for a given source image and scrape search results
import time
from MySQLdb import Timestamp
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.options import Options
import datetime
import sys


def main(source_url, no_results, name, timestamp, max_results):

    # number of pages processed
    pages = 1

    # selenium webdriver settings
    # TODO: choose your local path to the downloaded webdriver
    webdriver_path = '/Users/work/GitHub/plexxxi/webdriver/chromedriver'
    # the options object can store settings for your zombie browser
    options = Options()
    # choose incognito mode to open a private window mode
    options.add_argument("--incognito")
    # for testing on your local computer with a GUI, have chrome installed and uncomment line below
    options.add_argument("--headless")
    # headless browsing works without GUI but needs fix window size for infinite scroll scraping
    options.add_argument("window-size=1920,1080")

    # options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    language_code = 'en'
    # google_isearch = 'https://www.google.com/imghp'
    google_isearch = 'https://images.google.com/imghp?hl=' + \
        language_code + '&gl=' + language_code

    driver = webdriver.Chrome(webdriver_path, options=options)

    try:
        driver.get(google_isearch)
        driver.find_element_by_xpath('//*[@id="L2AGLb"]/div').click()
        time.sleep(4)
    except Exception as e:
        print(e)

    # driver.get(google_isearch)
    google_ris_button = None
    try:
        google_ris_button = driver.find_element_by_xpath(
            '//*[@id="sbtc"]/div/div[3]/div[2]/span')
    except Exception as e:
        google_ris_button = driver.find_element_by_xpath(
            '//*[@id="sbtc"]/div[1]/div/div[3]/div[2]/span')
        print('Take another button')

    time.sleep(2)

    try:
        google_ris_button.click()
        time.sleep(5)
        search_input = driver.find_element_by_xpath('//*[@id="Ycyxxc"]')
        search_input.send_keys(source_url)
        time.sleep(2)
        submit_btn = driver.find_element_by_xpath('//*[@id="RZJ9Ub"]').click()
        time.sleep(5)

        # fetch data
        try:

            # if not max_results:
            #     pages = round(int(no_results) / 10)

            # for i in range(0, pages):
            while True:
                htmlcontent = driver.page_source
                Path('htmlfiles/').mkdir(parents=True, exist_ok=True)
                Path('htmlfiles/' + name + '/').mkdir(parents=True, exist_ok=True)
                fh = open('htmlfiles/' + name + '/page_' +
                          str(pages) + '_at_' + timestamp + '.html', 'w')
                fh.write(htmlcontent)

                time.sleep(4)
                if not max_results:
                    if pages >= round(int(no_results) / 10):
                        break
                try:
                    next_button = driver.find_element_by_xpath(
                        '//*[@id="pnnext"]')
                    driver.execute_script(
                        "arguments[0].scrollIntoView();", next_button)
                    next_button.click()
                    pages = pages + 1
                    print('Processed page ' + pages)
                except Exception as e:
                    break

        except Exception as e:
            print(str(e) + ' fetching data unsucessful')
            driver.quit()
    except Exception as e:
        print(str(e) + ' search action unsuccessful')
        driver.quit()

    driver.quit()
    return pages


if __name__ == "__main__":
    url = sys.argv[1]
    no_results = sys.argv[2]
    name = sys.argv[3]
    timestamp = sys.argv[4]
    max_results = sys.argv[5]
    main(url, no_results, name, timestamp, max_results)
