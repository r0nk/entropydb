#!/bin/bash

if [ $[ $RANDOM % 2 ] = 0 ]; then
	cat test.json  | sed "s/REPLACEME/$RANDOM/g" | http POST http://127.0.0.1:5000
else
	cat test.json  | sed "s/REPLACEME/$RANDOM/g;s/rep2/$RANDOM/g" | http POST http://127.0.0.1:5000
fi

