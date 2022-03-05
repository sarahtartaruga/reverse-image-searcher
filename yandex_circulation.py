# this script retrieves matching pages and similar images for a given image

import yandex_info_pages_to_csv
import yandex_similar_images_to_csv
import sys


url = sys.argv[1]
no_results = sys.argv[2]
name = sys.argv[3]

yandex_info_pages_to_csv.main(url, no_results, name)
yandex_similar_images_to_csv.main(url, no_results, name)
