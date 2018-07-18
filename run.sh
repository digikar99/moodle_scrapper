#!/bin/bash

truncate -s 0 res.json
scrapy crawl moodle --nolog -o res.json
