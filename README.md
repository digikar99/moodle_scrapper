# IITB MOODLE SCRAPPER (made in 2018)

Check for moodle updates automatically. Currently only announcements and links are supported.

## DEPENDENCIES

Requires python 2.7 and scrapy 1.4. Python is usually paxked with your disctribution. To install scrapy, run

    sudo apt update && sudo apt install python-scrapy

Also ensure you have google-chrome if you want to open updated course pages in browser.

## OTHER INSTRUCTIONs

Download/Clone the repository (check this page in Desktop mode) and extract it at a location of your choice. Ensure you can access moodle: currently it does not report whether connection failed. Though you can remove the "--nolog"  option in run.sh to check the logs.

To open links in google-chrome, keep yourself logged in moodle on google-chrome.

## RUNNING the moodle_scrapper

    chmod +x run.sh

and run:

    ./run.sh
