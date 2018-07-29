#!/bin/bash

touch .auth
n_auth=$(wc -l .auth)
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
	touch json/old.json
	truncate -s 0 links.json
	truncate -s 0 json/new.json

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

truncate -s 0 json/new.json
printf "Checking for announcements...\n"

## Remove the --nolog option to debug
scrapy crawl moodle --nolog <<< $(printf "$user\n$pass\n$n_courses\n$first_time\n")

sorted_pretty=$(sort "json/new.json" | python -m json.tool)
cat <<< "$sorted_pretty" > "json/new.json"

changes=$(diff --unified json/old.json json/new.json | grep -E "^\+" | tail -n +2)

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
		cp json/new.json json/old.json
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
