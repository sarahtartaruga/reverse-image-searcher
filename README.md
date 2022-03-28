# Reverse Image Searcher
This is a Python script to study the circulation of an image on the web by conducting reverse image search. The script can conduct a reverse image search on Google and/or Yandex for a given image url of interest. It does retrieve 
1) for Google all suggested **visually similar images** or for Yandex all **similar images**, and 
2) for Google all **pages that include matching images** or for Yandex all **sites containing information about the image**. 

As an output you retrieve the data for your project in separate folders for Yandex and Google in separate folders for the matching pages and the similar images, with html, thumbnail image and csv files. More details can be found in the following.

## Requirements
You need to download the [Selenium Chrome driver](https://chromedriver.chromium.org/getting-started) fitting your locally installed version of Google Chrome to run the configured headless zombie browser. Store the downloaded driver 

## Matching