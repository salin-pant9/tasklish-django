#!/usr/bin/env bash

# Variables
URL="http://localhost:8000"

# Login
Token=$(./login.sh safal safal12345 | jq -r .token)

if [[ $Token == null ]]; then
	echo "[-] Login Failed. Exiting....."
	exit
fi

curl --silent "$URL/boards/create" \
	--header 'Content-Type: application/json' \
	--header 'Accept: application/json' \
	--header "Authorization: Token $Token" \
	--data '
  {
    "name": "Test Board",
    "description": "This is a test board"
  }' | jq
