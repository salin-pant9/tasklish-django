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

curl --silent "$URL/boards/add-hours/$board_id" \
	-X PUT \
	--header 'Content-Type: application/json' \
	--header 'Accept: application/json' \
	--header "Authorization: Token $Token" \
	--data '
  {
    "monday": [{ "start": "9:00", "end": "18:00" }],
    "tuesday": [{ "start": "9:00", "end": "18:00" }],
    "thursday": [{ "start": "9:00", "end": "18:00" }],
    "wednesday": [{ "start": "9:00", "end": "18:00" }],
    "friday": [{ "start": "9:00", "end": "18:00" }],
    "saturday": [{ "start": "9:00", "end": "18:00" }],
    "sunday": [{ "start": "9:00", "end": "18:00" }]
  }'
