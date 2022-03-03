# this script downloads all thumbnails from csv file and adds new column in csv with their local path
import pandas as pd
from pathlib import Path
import base64
import sys

# read the thumbnail urls from csv file and return them in a list


def read_rows(path):
    with open(path) as f:
        df = pd.read_csv(f)
        # read data of one column into a list
        column = df['thumbnail_url']
        f.close()
        return column


def main(csv_path, dirname):
    results = read_rows(csv_path)

    i = 1
    fnames = []
    for result in results:

        try:
            data = result.replace('data:image/jpeg;base64,', '')

            basedir = 'thumbnails/'
            Path(basedir).mkdir(parents=True, exist_ok=True)
            Path(basedir + dirname).mkdir(parents=True, exist_ok=True)
            fname = basedir + dirname + 'thumbnail_' + str(i) + '.png'
            try:
                with open(fname, 'wb') as f:
                    f.write(base64.b64decode(data))
                    f.close()
                    fnames.append(fname)
                    print("%s decoded!\n" % fname)
            except Exception as e:
                print('Image data not decoded ' + str(e))
                fnames.append(None)
        except Exception as e:
            print('Decoding set up went wrong ' + str(e))
            fnames.append(None)
        i = i + 1

    with open(csv_path) as f:
        df = pd.read_csv(f)
        df['thumbnail_path'] = fnames
        csv_fname = csv_path.replace('.csv', '') + '_with_thumbnail_paths.csv'
        df.to_csv(csv_fname, index=False)
        f.close()


if __name__ == "__main__":
    # csv_path = '/Users/work/GitHub/circulation/csvfiles/ukraine_kindergarden/314_results_scraped_at_2022-03-03_09-09-28.csv'
    # dirname = 'ukraine_kindergarden/'
    csv_path = sys.argv[1]
    dirname = sys.argv[2]
    main(csv_path, dirname)
