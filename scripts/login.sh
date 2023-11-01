#!/usr/bin/env bash
#################################################################
# Help
#################################################################
Help()
{
  echo "Login script for Tasklish, sends JSON data with username and password to "
  echo "retrieve the API token."
  echo
  echo "Syntax: login.sh <username> <password>"
  echo
}

if [ $# -ne 2 ]; then
	Help
	exit
fi

# Get the options
while getopts ":h" option; do
	case $option in
		h) # display help
			Help
			exit;;
	esac
done


# Variables
URL="http://localhost:8000"


# Login
username=$1
password=$2

curl --silent -X POST "$URL/users/login" \
	--header 'Content-Type: application/json' \
	--header 'Accept: application/json' \
	--data '
	{
	  "username": "'"$username"'",
	  "password": "'"$password"'"
	}' | jq


