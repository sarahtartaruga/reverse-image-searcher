# this script retrieves matching pages and similar images for a given image via yandex reverse image search

import google_matching_pages_to_csv
import google_similar_images_to_csv
import sys


def main(url, no_results, name, country_code, host_language):
    google_matching_pages_to_csv.main(
        url, no_results, name, country_code, host_language)
    google_similar_images_to_csv.main(
        url, no_results, name, country_code, host_language)


if __name__ == "__main__":
    url = sys.argv[1]
    no_results = sys.argv[2]
    name = sys.argv[3]
    country_code = sys.argv[4]
    host_language = sys.argv[5]
    main(url, no_results, name, country_code, host_language)
