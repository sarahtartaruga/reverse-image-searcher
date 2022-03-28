import google_circulation
import yandex_circulation
import sys

url = sys.argv[1]
no_results = sys.argv[2]
name = sys.argv[3]
country_code = sys.argv[4]
host_language = sys.argv[5]

try:
    engine = sys.argv[6]
    if engine == 'google':
        print('Conduct reverse image search to retrieve search results and at maximum ' + str(no_results) +
              ' similar images for Google for the project ' + name + ' and image url ' + url)
        google_circulation.main(url, no_results, name,
                                country_code, host_language)
    elif engine == 'yandex':
        print('Conduct reverse image search to retrieve search results and at maximum ' + str(no_results) +
              ' similar images for Yandex for the project ' + name + ' and image url ' + url)
        yandex_circulation.main(url, no_results, name)
except Exception as e:
    print('Conduct reverse image search to retrieve search results and at maximum ' + str(no_results) +
          ' similar images for Google and Yandex for the project ' + name + ' and image url ' + url)
    google_circulation.main(url, no_results, name, country_code, host_language)
    yandex_circulation.main(url, no_results, name)
