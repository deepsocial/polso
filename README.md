polso
=====

Tools for scraping Twitter/Facebook/WWW


# AMIS Scraper

This package contains tools for scraping data from

* bloomberg.com
* nogger-noggersblog.blogspot.it
* world-grain.com
* euractiv.com
* agrimoney.com

in orrder to construct a crisis prediction model based on a sentiment index.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

`Virtualenv` is required to ensure the dependencies are identical accross
different developers.

First install `virtualenv`.

```
pip install virtualenv
```

Then create the directory to store the packages.

```
virtualenv venv/
```

After the `virtualenv` has been installed, we can then activate the
`virtualenv`.

```
source venv/bin/activate
```

You should see your prompt modified with `(venv)` concatenated at the beginning.

After the activation, you can then install the current dependency based on the
`requirements.txt`.

```
pip install -r requirements.txt
```

Once you are done and finished working, deactivate the `virtualenv` by

```
deactivate
```

The `virtualenv` should be invoked every single time you start working on the
project.

To update the `requirement.txt`, simply run the following within the virtual
environment.

```
pip freeze > requirements.txt
```

### Running the Scraper

The scraping Machine can be run automatically

```
python amis_runner.py
```
or single sources can be scraped

```
scrapy crawl <spider name>
```

where the available spiders are

* bloomberg
* noggers
* worldgrain
* euractiv
* agrimoney

# Twitter scraper

A new twitter scraper using Abby's list of followers.
The xlsx file with the list of followers has been shared from Adam the 16Feb2017 and stored in the `data` folder.
The script requires python3 and it is able to download all twitter from the creation of the account (information present in the xlsx file).

The script works in two steps:

```
python3 twitter_scraper/scrape_from_list.py
```
This file create a json file for each follower with the ids of the twits.

The second step download the actual data:

```
python3 twitter_scraper/get_metadata.py
```
