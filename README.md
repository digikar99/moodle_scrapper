# IITB MOODLE SCRAPPER (made in 2018)

Check for moodle updates automatically. Currently only announcements and links are supported.

## DEPENDENCIES

Should work with python3.

```
    scrapy
	portego
```

## OTHER INSTRUCTIONs

Download/Clone the repository (check this page in Desktop mode) and extract it at a location of your choice. Ensure you can access moodle: currently it does not report whether connection failed. Though you can remove the "--nolog"  option in run.sh to check the logs.

To open links in google-chrome, keep yourself logged in moodle on google-chrome.

## RUNNING the moodle_scrapper

    chmod +x run.sh

and run:

    ./run.sh
    
## WARNING

Do NOT use this on a mass scale, else IITB moodle servers may overload!
