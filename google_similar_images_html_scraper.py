# this script enables to retrieve similar image data of an image  as proposed by Google reverse image search

import time
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.options import Options
import sys

def main(source_url, no_results, name, country_code, host_language, timestamp):

    # first step: conduct reverse image search
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

    google_isearch = 'https://images.google.com/imghp?hl=' + \
        host_language + '&gl=' + country_code

    driver = webdriver.Chrome(webdriver_path, options=options)

    # click cookie consent
    try:
        driver.get(google_isearch)
        driver.find_element_by_xpath('//*[@id="L2AGLb"]/div').click()
        time.sleep(4)
    except Exception as e:
        print('Issue with consent')
        print(e)

    # image search setup
    google_ris_button = None
    try:
        google_ris_button = driver.find_element_by_xpath(
            '//*[@id="sbtc"]/div/div[3]/div[2]/span')
    except Exception as e:
        google_ris_button = driver.find_element_by_xpath(
            '//*[@id="sbtc"]/div[1]/div/div[3]/div[2]/span')
        print('Take another button')

    time.sleep(2)

    # search google images for source image
    try:
        google_ris_button.click()
        time.sleep(5)
        search_input = driver.find_element_by_xpath('//*[@id="Ycyxxc"]')
        search_input.send_keys(source_url)
        time.sleep(2)
        submit_btn = driver.find_element_by_xpath('//*[@id="RZJ9Ub"]').click()
        time.sleep(5)

    except Exception as e:
        print('Issue with searching for source url')
        print(e)

 # second step: head to similar images
    try:
        link_to_similar_images = driver.find_element_by_xpath(
            '//*[@id="rso"]/div[2]/div/div[2]/g-section-with-header/div[1]/title-with-lhs-icon/a').click()

    except Exception as e:
        print('Issue with heading to similar images')
        print(e)

    # third step: scroll down as long as result amount corresponds with wished result
    results = []
    try:
        while len(results) < int(no_results):
            old_amount_results = len(results)
            print('Current amount of results : ' + str(len(results)))
            results = driver.find_elements_by_css_selector(
                "div[class='isv-r PNCib MSM1fd BUooTd']")
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            if old_amount_results == len(results):
                break
    except Exception as e:
        print('Issue with scrolling ' + str(e))

    # fourth step: save html data
    try:
        time.sleep(3)
        htmlcontent = driver.page_source
        Path('data/').mkdir(parents=True, exist_ok=True)
        Path('data/google/').mkdir(parents=True, exist_ok=True)
        Path('data/google/similar_images/').mkdir(parents=True, exist_ok=True)
        Path(
            'data/google/similar_images/htmlfiles/').mkdir(parents=True, exist_ok=True)
        Path('data/google/similar_images/htmlfiles/' +
             name + '/').mkdir(parents=True, exist_ok=True)
        fh = open('data/google/similar_images/htmlfiles/' + name + '/country_code_' +
                  country_code + '_host_lang_' + host_language + '_at_' + timestamp + '.html', 'w')
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
    country_code = sys.argv[4]
    host_language = sys.argv[5]
    timestamp = sys.argv[6]

    main(url, no_results, name, country_code, host_language, timestamp)
