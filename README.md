# Reverse Image Searcher
This is a Python based repository to study the circulation of an image on the web quantitatively by conducting reverse image search (across search engines). The script can conduct a reverse image search on Google and/or Yandex for a given image url of interest. It does retrieve 
1) for Google, all suggested **visually similar images**, or for Yandex all **similar images**, and 
2) for Google, all **pages that include matching images**, or for Yandex all **sites containing information about the image**. 

As an output you retrieve the data for your project in separate folders for Yandex and Google in separate folders for the matching pages and the similar images, with html, thumbnail image and csv files. More details can be found in the following.

## Quick start
To run the reverse image search for both *Google* and *Yandex* run

```python3 main.py url amount_similar_images project_name country_code_google host_language_google```

Example:

```python3 main.py 'https://www.howardshome.com/wp-content/uploads/2012/10/social-media-als-bron.jpg' 100 fake_news us en```

For using only *Google* or *Yandex* run 

```python3 main.py url amount_similar_images project_name country_code_google host_language_google search_engine_option```

With the ```search_engine_option``` being either ```google``` or ```yandex```.


Example *Google*:

```python3 main.py 'https://www.howardshome.com/wp-content/uploads/2012/10/social-media-als-bron.jpg' 100 fake_news us en google```

Example *Yandex*: 

Attention: the host language and country code do not apply here to the reverse image search

```python3 main.py 'https://www.howardshome.com/wp-content/uploads/2012/10/social-media-als-bron.jpg' 100 fake_news us en yandex```
## Pre-requisites

### Python 3 & packages
Make sure you have [Python3](https://www.python.org/downloads/) and the following packages installed:

 - time
- selenium
- pathlib
- datetime
- bs4
- csv
### Download repository
Download this repository to your computer.
### Selenium driver
You need to download the [Selenium Chrome driver](https://chromedriver.chromium.org/getting-started) fitting your locally installed version of Google Chrome to run the configured headless zombie browser. Store the downloaded driver executable file in the repository folder.

## General Procedure

The general outset is that you have an image (as url) of interest where you are interested in seeing how it circulates the web, meaning how search engines propose similar images or other related information to the image. The script works in the way that it opens a zombie browser that enters the image search for either [Google](https://images.google.com/imghp) or [Yandex](https://yandex.com/images/). By simulating a click on the reverse image button, the url is then pasted into the search bar. The result page delivers similar images and websites as search results that relate to your image. The zombie browser goes through the search results and the relevant information is then stored (delivering image, html, csv data as output). 

For the related websites on Google, the browser goes through **all** available pages and stores the html file first, from which details are extracted separately. For the similar images on Google, there is a simulated scroll that scrolls until the desired amount of images is reached.

For the related websites on Yandex and the similar images, there is a simulated scroll that scrolls until the desired amount of images and search results is reached. 
## Google Reverse Image Search
### Regional settings
For the reverse image search on *Google* you can set regional settings via the **country code** and **host language** options that are integrated to your query that leads to you to the reverse image search on *Google*:

`` 'https://images.google.com/imghp?hl=' + \
        host_language + '&gl=' + country_code ``
        
Be aware that your search is still impacted by your IP address and the output is therefore always to some extent biased towards your local machine and location. 

### Affordances
For *Google*, the following affordances are taken into account:

- Visually similar images
- Pages that include matching images

On [this website](https://smartframe.io/blog/google-reverse-image-search-everything-you-need-to-know/) more information can be found on the workings of these search engine affordances.
### Output

The output will be stored under `data\google` with two separate folders:

- `data\google\matching_pages`
- `data\google\similar_images`
  
For the **matching pages**, you find a csv file that contains all the delivered pages that include the image as proposed by *Google*. 

The ```csvfiles``` folder contains the csv file output that has following data included for the search results:

- *rank*
- possible related search query as suggested by Google (*possible_related_search*)
- *url*
- *domain*
- country code extracted from the domain (*country_code_tld*)
- *title* meaning the header of the search result
- *description* containing all of the information visible for the item 
- *text* containing only the text that is part of the description
- thumbnail resolution (*thumbnail_res*) that is part of the description but not always present 
- *date* being a date proposed by Google that is part of the description but not always present 
- thumbnail url (*thumbnail_url*) being the link to the thumbnail that is visible in the proposed search result
- thumbnail path (*thumbnail_path*) being the link to where the thumbnail file is stored locally on your computer

The ```htmlfiles``` folder contains the visited pages that is used to extract the data to a csv file. 

The ```thumbnails``` folder contains all thumbnails images as png files that are visible per search result. The data is downloaded and the path to each image file is in the csv file. Each thumbnail image starts with *thumbnail_x* with x being the rank of the related search result. This way, missing images and the order of appearance is kept intact. 


For the **similar images**, there is a csv file that contains information about the images as they appear in the search engine suggestion (from left to right and top to bottom). This file is stored in the ```csvfiles``` folder and contains the following data:

- *rank*
- *url*
- *domain*
- country code extracted from the domain (*country_code_tld*)
- *title* meaning the header of the search result
- info tag (*info_tag*) containing metadata that is visible for the item (e.g. whether the image is an ad, or a related date)
- thumbnail url (*thumbnail_url*) being the link to the image that is visible in the proposed search result
- thumbnail path (*thumbnail_path*) being the link to where the image file is stored locally on your computer

The rest of data storage (html files and image files) aligns to the structure of the matching pages affordance.
## Yandex Reverse Image Search
### Regional settings
After testing difference language settings for *Yandex*, it seems this option does not apply to the Image search on *Yandex* and is hence ignored. 

### Affordances
For *Yandex*, the following affordances are taken into account:

- Similar images
- Sites containing information about the image

### Output

The output will be stored under `data\yandex` with two separate folders:

- `data\yandex\info_pages`
- `data\yandex\similar_images`
  
For the **info pages**, you find a csv file that contains all the delivered pages that contain information about the image as proposed by *Yandex*. 

The ```csvfiles``` folder contains the csv file output that has following data included for the search results:

- *rank*
- *url*
- *domain*
- country code extracted from the domain (*country_code_tld*)
- *title* meaning the header of the search result
- *description* containing all of the information visible for the item 
- thumbnail resolution (*thumbnail_res*) that is part of the description but not always present 
- thumbnail url original (*thumbnail_url_original*) being the link to the original image file behind the thumbnail that is visible in the proposed search result
- thumbnail url (*thumbnail_url*) being the link to the thumbnail that is visible in the proposed search result
- thumbnail path (*thumbnail_path*) being the link to where the thumbnail file is stored locally on your computer

The ```htmlfiles``` folder contains the page html that is used to extract the data to a csv file. 

The ```thumbnails``` folder contains all thumbnails images as png files that are visible per search result. The data is downloaded and the path to each image file is in the csv file. Each thumbnail image starts with *thumbnail_x* with x being the rank of the related search result. This way, missing images and the order of appearance are kept intact. 

For the **similar images**, there is a csv file that contains information about the images as they appear in the search engine suggestion (from left to right and top to bottom). This file is stored in the ```csvfiles``` folder and contains the following data:

- *rank*
- *url*
- *domain*
- country code extracted from the domain (*country_code_tld*)
- *title* meaning the header of the search result
- thumbnail url (*thumbnail_url*) being the link to the image that is visible in the proposed search result
- thumbnail path (*thumbnail_path*) being the link to where the image file is stored locally on your computer

The rest of data storage (html files and image files) aligns to the structure of the matching pages affordance.


## Future directions

- There is ongoing work on a script that can visualise the outputs in a comparative fashion. 
- The project could be extended to include more search engines to conduct cross-engine research.  

## Usage

This repository addresses the interest of researchers and attempts to pay a contribution to societal oriented research. Feel free to use the code for your research and propose new functionalities or collaborate. 