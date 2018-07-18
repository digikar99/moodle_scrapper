#!/bin/bash

truncate -s 0 new_res.jl
printf "Checking for announcements...\n"
scrapy crawl moodle --nolog -o new_res.jl

sort res.jl > res_sort.jl
sort new_res.jl > new_res_sort.jl

changes=$(diff res_sort.jl new_res_sort.jl | tail -n +2)

if [ -z "$changes" ]
then
	printf "There are no new announcements.\n"
else
	printf "\nNew announcements:\n"
	printf "$changes"
fi

