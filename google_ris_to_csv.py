# this script deploys a reverse image search on google for a given source image and scrape search results
import csv
import time
import sys
from os import path
from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import google_ris_html_scraper


def main(source_url, no_results, name):

    # time of scraping run
    start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # scrape html content separately (can be disactivated if content has been scraped; but start_time must be adapted too)
    # start_time = '2022-03-02_11-32-29'

    max_results = True

    pages = google_ris_html_scraper.main(source_url, no_results, name, start_time, max_results)
    # pages = round(int(no_results) / 10)
    html_dir = 'htmlfiles/' + name + '/'
    csv_dir = 'csvfiles/' + name + '/'


    # list to store search results
    search_results = []

    possible_related_search = ''
    # read html content to extract information to csv
    for i in range(0, pages):
        fname = html_dir + 'page_' + \
            str(i+1) + '_at_' + start_time + '.html'
        with open(fname, 'r') as f:
            page_content = f.read()
            soup = BeautifulSoup(page_content, 'html.parser')

            if i == 0:
                possible_related_search = soup.find('a', {'class' : 'fKDtNb'}).text
            # retrieve search results per page
            results = soup.find_all('div', {'class': ['g', 'tF2Cxc']})
            print('Found search results on page ' +
                  str(i+1) + ' : ' + str(len(results)))

            for result in results:
                print(" NEWWWWWW RESULT !!!!!!!!!!!!!!!!!!!!")
                # print(result.prettify())
                search_result = {}

                search_result['rank'] = len(search_results)
                search_result['possible_related_search'] = possible_related_search

                try:
                    search_result['url'] = result.find(
                        'div', {'class': 'yuRUbf'}).find('a')['href']
                except Exception as e:
                    search_result['url'] = None
                try:
                    search_result['thumbnail_url'] = result.find(
                        'img', {'class': 'rISBZc zr758c'})['src']
                except Exception as e:
                    search_result['thumbnail_url'] = None

                try:
                    search_result['title'] = result.find(
                        'h3', {'class': 'LC20lb MBeuO DKV0Md'}).text
                except Exception as e:
                    search_result['title'] = None
                try:
                    container = result.find(
                        'div', {'class': ['VwiC3b', 'yXK7lf', 'MUxGbd', 'yDYNvb', 'lyLwlc']})

                    search_result['description'] = container.get_text()

                except Exception as e:
                    search_result['description'] = None

                try:
                    if ' × ' in search_result['description']:
                        search_result['thumbnail_res'] = search_result['description'].split('—')[
                            0].split(' · ')[0]
                    else:
                        search_result['thumbnail_res'] = None
                except Exception as e:
                    search_result['thumbnail_res'] = None

                try:
                    if ' · ' in search_result['description']:
                        date_tmp= search_result['description'].split(
                            ' · ')[-1].split('—')[0]
                        if date_tmp.replace('.', '').strip().isdecimal():
                            search_result['date'] = search_result['description'].split(
                                ' · ')[-1].split('—')[0]
                    else:
                        search_result['date'] = None
                except Exception as e:
                    search_result['date'] = None


                search_results.append(search_result)

                if not max_results:
                    if len(search_results) > int(no_results):
                        break

            f.close()
    # store data
    Path('csvfiles/').mkdir(parents=True, exist_ok=True)
    Path('csvfiles/' + name + '/').mkdir(parents=True, exist_ok=True)
    fname_csv = csv_dir + no_results + '_results_scraped_at_' + start_time + '.csv'
    keys = search_results[0].keys()
    with open(fname_csv, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(search_results)
        output_file.close()


if __name__ == "__main__":
    url = sys.argv[1]
    no_results = sys.argv[2]
    name = sys.argv[3]
    main(url, no_results, name)
