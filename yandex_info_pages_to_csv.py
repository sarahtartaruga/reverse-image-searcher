# this script deploys a reverse image search on google for a given source image and scrape search results
import csv
import sys
from os import path
from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import yandex_info_pages_scraper
import thumbnail_decoder


def main(source_url, no_results, name):
    country_code = 'us'
    host_language = 'en'

    # time of scraping run
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # scrape html content separately (can be disactivated if content has been scraped; but start_time must be adapted too)
    # start_time = '2022-03-03_09-09-28'

    max_results = True

    # create needed directories
    Path('data/').mkdir(parents=True, exist_ok=True)
    Path('data/yandex/').mkdir(parents=True, exist_ok=True)
    Path('data/yandex/info_pages/').mkdir(parents=True, exist_ok=True)

    yandex_info_pages_scraper.main(
        source_url, no_results, name, start_time, max_results, country_code, host_language)
    html_dir = 'data/yandex/info_pages/htmlfiles/' + name + '/'
    csv_dir = 'data/yandex/info_pages/csvfiles/' + name + '/'
    thumb_dir = 'data/yandex/info_pages/thumbnails/' + name + '_' + start_time + '/'

    # list to store search results
    search_results = []

    # read html content to extract information to csv
    fname = html_dir + start_time + '.html'

    with open(fname, 'r') as f:
        page_content = f.read()
        soup = BeautifulSoup(page_content, 'html.parser')
        f.close()

        results = soup.find_all(
            'div', {'class': 'CbirSites-Item'})
        print('Found ' + str(len(results)) + ' results')

        for result in results:
            search_result = {}
            print('Processing search result no ' +
                  str(len(search_results) + 1))

            search_result['rank'] = len(search_results)

            try:
                search_result['url'] = result.find(
                    'div', {'class': 'CbirSites-ItemTitle'}).find('a')['href']
            except Exception as e:
                search_result['url'] = None
                print('No url found ' + str(e))

            try:
                search_result['domain'] = result.find(
                    'a', {'class': 'CbirSites-ItemDomain'}).text
            except Exception as e:
                search_result['domain'] = None
                print('No domain found ' + str(e))

            try:
                search_result['country_code_tld'] = search_result['domain'].split(
                    '.')[-1]
            except Exception as e:
                search_result['country_code_tld'] = None
                print('No country code found ' + str(e))

            try:
                search_result['title'] = result.find(
                    'div', {'class': 'CbirSites-ItemTitle'}).find('a').text
            except Exception as e:
                search_result['title'] = None
                print('No title found ' + str(e))

            try:
                search_result['description'] = result.find(
                    'div', {'class': 'CbirSites-ItemDescription'}).text
            except Exception as e:
                search_result['description'] = None
                print('No info tag found ' + str(e))

            try:
                search_result['thumbnail_res'] = result.find(
                    'div', {'class': 'Thumb-Mark Typo Typo_text_s'}).text
            except Exception as e:
                search_result['thumbnail_res'] = None
                print('No thumbnail res found ' + str(e))

            try:
                # large thumbnails
                search_result['thumbnail_url_original'] = result.find(
                    'a', {'class': 'Thumb_type_inline'})['href']
                # search_result['thumbnail_url'] = 'https:' + result.find(
                #     'img', {'class': 'Thumb-Image'})['src']
            except Exception as e:
                search_result['thumbnail_url_original'] = None
                print('No thumbnail url found ' + str(e))

            try:
                # small thumbnails
                search_result['thumbnail_url'] = 'https:' + result.find(
                    'img', {'class': 'Thumb-Image'})['src']
            except Exception as e:
                search_result['thumbnail_url'] = None
                print('No thumbnail url found ' + str(e))

            search_results.append(search_result)
            if len(search_results) >= int(no_results):
                break

        f.close()
    # store data
    Path('data/yandex/info_pages/csvfiles/').mkdir(parents=True, exist_ok=True)
    Path(csv_dir).mkdir(parents=True, exist_ok=True)
    fname_csv = csv_dir + str(len(search_results)) + \
        '_results_scraped_at_' + start_time + '.csv'
    keys = search_results[0].keys()
    with open(fname_csv, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(search_results)
        output_file.close()

    # sixth step: from csv file retrieve thumbnails
    thumbnail_decoder.main(fname_csv, thumb_dir)


if __name__ == "__main__":
    url = sys.argv[1]
    no_results = sys.argv[2]
    name = sys.argv[3]
    main(url, no_results, name)
