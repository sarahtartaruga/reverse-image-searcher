# this script enables to retrieve similar image data of an image  as proposed by Google reverse image search

from pathlib import Path
import datetime
from bs4 import BeautifulSoup
import csv
import sys
import google_similar_images_html_scraper
import thumbnail_decoder


def main(source_url, no_results, name, country_code, host_language):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # timestamp = '2022-03-05_13-15-57'

    # first step: conduct reverse image search and store html files

    # first step: conduct reverse image search and store html files
    # add on: if data has been scraped you can uncomment this line, adapt timestamp respectively and pass same name
    google_similar_images_html_scraper.main(
        source_url, no_results, name, country_code, host_language, timestamp)

    # from html data retrieve relevant data as csv file

    # list to store search results
    search_results = []

    html_dir = 'data/google/similar_images/htmlfiles/' + name + '/'
    csv_dir = 'data/google/similar_images/csvfiles/' + name + '/'
    thumb_dir = 'data/google/similar_images/thumbnails/' + name + '_' + timestamp + '/'

    # open html file
    fname = html_dir + 'country_code_' + country_code + \
        '_host_lang_' + host_language + '_at_' + timestamp + '.html'

    with open(fname, 'r') as f:
        page_content = f.read()
        soup = BeautifulSoup(page_content, 'html.parser')
        f.close()

        # results = soup.find_all(
        #     'div', {'class': ['isv-r', 'PNCib', 'MSM1fd', 'BUooTd']})
        results = soup.find_all(
            'div', {'class': 'isv-r PNCib MSM1fd BUooTd'})
        print('Found ' + str(len(results)) + ' results')

        for result in results:
            search_result = {}
            print('Processing search result no ' +
                  str(len(search_results) + 1))

            search_result['rank'] = len(search_results)

            try:
                search_result['url'] = result.find(
                    'a', {'class': ['VFACy', 'kGQAp', 'sMi44c', 'lNHeqe', 'WGvvNb']})['href']
            except Exception as e:
                search_result['url'] = None
                print('No url found ' + str(e))

            try:
                search_result['domain'] = result.find(
                    'a', {'class': ['VFACy', 'kGQAp', 'sMi44c', 'lNHeqe', 'WGvvNb']}).find('div', {'class': 'fxgdke'}).text
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
                    'a', {'class': ['VFACy', 'kGQAp', 'sMi44c', 'lNHeqe', 'WGvvNb']})['title']
            except Exception as e:
                search_result['title'] = None
                print('No title found ' + str(e))

            try:
                search_result['info_tag'] = result.find(
                    'span', {'class': ['dP3z3e', 'UavG3d']}).text
            except Exception as e:
                search_result['info_tag'] = None
                print('No info tag found ' + str(e))

            try:
                search_result['thumbnail_url'] = result.find(
                    'img', {'class': 'rg_i Q4LuWd'})['src']
            except Exception as e:
                search_result['thumbnail_url'] = None
                print('No thumbnail url found ' + str(e))

            search_results.append(search_result)
            if len(search_results) >= int(no_results):
                break

        f.close()
    # store data
    Path('data/google/similar_images/csvfiles/').mkdir(parents=True, exist_ok=True)
    Path(csv_dir).mkdir(parents=True, exist_ok=True)
    fname_csv = csv_dir + str(len(search_results)) + \
        '_results_country_code_' + country_code + '_host_lang_' + \
        host_language + '_scraped_at_' + timestamp + '.csv'
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
    country_code = sys.argv[4]
    host_language = sys.argv[5]
    main(url, no_results, name, country_code, host_language)
