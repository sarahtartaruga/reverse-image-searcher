# this script deploys a reverse image search on yandex for a given source image and scrapes 'Sites containing information about the image'
import time
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.options import Options
import sys


def main(source_url, no_results, name, timestamp):

    # number of pages processed
    pages = 1

    # selenium webdriver settings
    # TODO: choose your local path to the downloaded webdriver
    webdriver_path = './chromedriver'
    # the options object can store settings for your zombie browser
    options = Options()
    # choose incognito mode to open a private window mode
    options.add_argument("--incognito")
    # for testing on your local computer with a GUI, have chrome installed and uncomment line below
    options.add_argument("--headless")
    # headless browsing works without GUI but needs fix window size for infinite scroll scraping
    options.add_argument("window-size=1920,1080")

    yandex_isearch = 'https://yandex.com/images/'
    # does usually not deliver any results
    # yandex_isearch_language = 'https://yandex.com/images/search?text=ukraine+lang%3A' + host_language

    driver = webdriver.Chrome(webdriver_path, options=options)

    try:
        driver.get(yandex_isearch)
        time.sleep(2)
    except Exception as e:
        print(e)

    ris_button = None
    try:
        ris_button = driver.find_element_by_xpath(
            '/html/body/header/div/div[2]/div[1]/form/div[1]/span/span/button/div')
    except Exception as e:
        # google_ris_button = driver.find_element_by_xpath(
        #     '//*[@id="sbtc"]/div[1]/div/div[3]/div[2]/span')
        print('Take another button ' + str(e))

    time.sleep(2)

    try:
        ris_button.click()
        time.sleep(5)
        search_input = driver.find_element_by_xpath(
            '/html/body/header/div/div[3]/div[1]/form/span/input')
        search_input.send_keys(source_url)
        time.sleep(2)
        submit_btn = driver.find_element_by_xpath(
            '/html/body/header/div/div[3]/div[1]/form/button').click()
        time.sleep(5)
    except Exception as e:
        print('Could not submit query correctly: ' + str(e))

        # container: //*[@id="CbirSites_infinite-NzQkc36"]/section

        # fetch data

    # third step: scroll down as long as result amount corresponds with wished result
    results = []
    try:
        scroll_counter = 1
        while len(results) < int(no_results):
            old_amount_results = len(results)
            print('Current amount of results : ' + str(len(results)))
            results = driver.find_elements_by_css_selector(
                "div[class='CbirSites-Item']")
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            # driver.execute_script(
            #     "window.scrollTo(0," + str(500 * scroll_counter) + ")")
            # time.sleep(1)
            scroll_counter = scroll_counter + 1
            if old_amount_results == len(results):
                print('After ' + str(scroll_counter) +
                      ' scrolls amount is the same')
                break
    except Exception as e:
        print('Issue with scrolling ' + str(e))

    # fourth step: save html data
    try:
        time.sleep(3)
        htmlcontent = driver.page_source
        Path('data/').mkdir(parents=True, exist_ok=True)
        Path('data/yandex/').mkdir(parents=True, exist_ok=True)
        Path('data/yandex/info_pages/').mkdir(parents=True, exist_ok=True)
        Path(
            'data/yandex/info_pages/htmlfiles/').mkdir(parents=True, exist_ok=True)
        Path('data/yandex/info_pages/htmlfiles/' +
             name + '/').mkdir(parents=True, exist_ok=True)
        fh = open('data/yandex/info_pages/htmlfiles/' +
                  name + '/' + timestamp + '.html', 'w')
        fh.write(htmlcontent)
        fh.close()

    except Exception as e:
        print('Issue with saving html')
        print(e)

    # close driver when finished
    driver.quit()


if __name__ == "__main__":
    url = sys.argv[1]
    no_results = sys.argv[2]
    name = sys.argv[3]
    timestamp = sys.argv[4]
    # max_results = sys.argv[5]
    # country_code = sys.argv[6]
    # host_language = sys.argv[7]
    main(url, no_results, name, timestamp)
