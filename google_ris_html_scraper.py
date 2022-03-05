# this script deploys a reverse image search on google for a given source image and scrape search results
import time
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.options import Options
import sys

def main(source_url, no_results, name, timestamp, max_results, country_code, host_language):

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

    # country_code = 'en'
    # # German host language is set to easily retrieve date
    # host_language = 'de'

    google_isearch = 'https://images.google.com/imghp?hl=' + \
        host_language + '&gl=' + country_code

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
                Path('data/').mkdir(parents=True, exist_ok=True)
                Path('data/google/').mkdir(parents=True, exist_ok=True)
                Path('data/google/matching_pages/').mkdir(parents=True, exist_ok=True)
                Path(
                    'data/google/matching_pages/htmlfiles/').mkdir(parents=True, exist_ok=True)
                
                Path('data/google/matching_pages/htmlfiles/' +
                     name + '_' + timestamp + '/').mkdir(parents=True, exist_ok=True)
                fh = open('data/google/matching_pages/htmlfiles/' + name + '_' + timestamp + '/page_' +
                          str(pages) + '_' + country_code + '_host_lang_' +
                          host_language + '_at_' + timestamp + '.html', 'w')
                fh.write(htmlcontent)

                time.sleep(4)
                if max_results == False:
                    if pages > round(int(no_results) / 10):
                        print('Achieved result number')
                        break
                try:
                    next_button = driver.find_element_by_xpath(
                        '//*[@id="pnnext"]')
                    driver.execute_script(
                        "arguments[0].scrollIntoView();", next_button)
                    next_button.click()
                    print('Processed page ' + str(pages))
                    pages = pages + 1
                except Exception as e:
                    print('Something went wrong with clicking next button ' + str(e))
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
    country_code = sys.argv[6]
    host_language = sys.argv[7]
    main(url, no_results, name, timestamp,
         max_results, country_code, host_language)
