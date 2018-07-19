#!/bin/bash

touch .auth
n_auth=$(wc -l .auth) # .auth file will be present in the package!
user=""
pass=""
n_courses=""
first_time=""

# Try to guess if .auth file is in proper condition
if [ "$n_auth" != "3 .auth" ]
then
# If not in proper condition...
	printf "Username: "
	read user
	printf "Password: "
	read -s pass
	printf "\nNumber of courses: "
	read n_courses

	first_time="yes"
	touch links.json
	truncate -s 0 links.json

	printf "Would you like to save this information? (y/[n])\n(Passwords would be saved in plain text file named .auth, without any encryption. This may be fixed in a future update.)"
	read save

	if [ "$save" = "y" ] || [ "$save" = "Y" ]
	then
		printf "Yes\n"
		to_save="$user\n$pass\n$n_courses\n"
		printf "$to_save" > .auth
	fi
else
	mapfile -t myarr < .auth
	user=${myarr[0]}
	pass=${myarr[1]}
	n_courses=${myarr[2]}
	first_time="no"
fi

## CHECK FOR UPDATES

#truncate -s 0 jl/new_res.jl
printf "Checking for announcements...\n"
#scrapy crawl moodle -o jl/new_res.jl <<< $(printf "$user\n$pass\n$n_courses\n$first_time\n")

sort jl/res.jl > jl/res_sort.jl
sort jl/new_res.jl > jl/new_res_sort.jl

changes=$(diff --unified jl/res_sort.jl jl/new_res_sort.jl | grep -E "^\+" | tail -n +2)

if [ -z "$changes" ]
then
	printf "There are no new announcements. (Or the username or password may be incorrect.)\n"
else
	printf "\n================NEW UPDATES==============\n"
	printf "$changes\n"
	grep -o '".*"' <<< "$changes" | awk -F"\"" '{print $2}' > changes.txt
	printf "\nWould you like to save these changes? ([y]/n)"
	read save
	if [ "$save" = "n" ] || [ "$save" = "N" ]
	then
		printf "No\n"
	else
		printf "Yes\n"
		cp jl/new_res_sort.jl jl/res_sort.jl
		cp jl/new_res.jl jl/res.jl
	fi
	printf "\nWould you like to open the links with changes in browser? ([y]/n)"
	read save
	if [ "$save" = "n" ] || [ "$save" = "N" ]
	then
		printf "No\n"
		exit
	else
		printf "Yes\n"
		google-chrome $(python return_links.py)
	fi
fi
