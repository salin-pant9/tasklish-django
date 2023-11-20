#!/usr/bin/env bash

# Variables
URL="http://localhost:8000"

# Login
Token=$(./login.sh safal safal12345 | jq -r .token)

if [[ $Token == null ]]; then
	echo "[-] Login Failed. Exiting....."
	exit
fi

board_id=$1

if [[ $board_id == "" ]]; then
	echo "[-] Board ID not provided. Exiting....."
	exit
fi

curl --silent "$URL/boards/get-hours/$board_id" \
	-X GET \
	--header 'Content-Type: application/json' \
	--header 'Accept: application/json' \
	--header "Authorization: Token $Token" | jq
