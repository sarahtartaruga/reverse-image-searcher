# this script retrieves matching pages and similar images for a given image

import google_matching_pages_to_csv
import google_similar_images_to_csv
import sys


url = sys.argv[1]
no_results = sys.argv[2]
name = sys.argv[3]

google_matching_pages_to_csv.main(url, no_results, name)
google_similar_images_to_csv.main(url, no_results, name)
