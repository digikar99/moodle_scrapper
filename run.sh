#!/bin/bash

touch .auth
n_auth=$(wc -l .auth) # .auth file will be present in the package!
user=""
pass=""
n_courses=""


if [ "$n_auth" != "3 .auth" ]
then
	printf "Username: "
	read user
	printf "Password: "
	read -s pass
	printf "\nNumber of courses: "
	read n_courses

	printf "Would you like to save this information? (y/[n])\n(Passwords would be saved in plain text file named .auth, without any encryption. This may be fixed in a future update.)"
	read save

	if [ "$save" = "y" ] || [ "$save" = "Y" ]
	then
		printf "Yes\n"
		to_save="$user\n$pass\n$n_courses\n"
		printf "$to_save" > .auth
	fi
fi

if [ -z "$user" ]
then
	mapfile -t myarr < .auth

	user=${myarr[0]}
	pass=${myarr[1]}
	n_courses=${myarr[2]}
fi


## CHECK FOR UPDATES

truncate -s 0 jl/new_res.jl
printf "Checking for announcements...\n"
scrapy crawl moodle --nolog -o jl/new_res.jl <<< $(printf "$user\n$pass\n$n_courses\n")

sort jl/res.jl > jl/res_sort.jl
sort jl/new_res.jl > jl/new_res_sort.jl

changes=$(diff --unified jl/res_sort.jl jl/new_res_sort.jl | grep -E "^\+" | tail -n +2)

if [ -z "$changes" ]
then
	printf "There are no new announcements. (Or the username or password may be incorrect.)\n"
else
	printf "\n================NEW UPDATES==============\n"
	printf "$changes\n"
	printf "\nWould you like to save these changes? ([y]/n)"
	read save
	if [ "$save" = "n" ] || [ "$save" = "N" ]
	then
		printf "No\n"
		exit
	else
		printf "Yes\n"
		cp jl/new_res_sort.jl jl/res_sort.jl
		cp jl/new_res.jl jl/res.jl
	fi
fi
