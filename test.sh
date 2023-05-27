#!/bin/bash

#if [ $[ $RANDOM % 2 ] = 0 ]; then
#cat test.json  | sed "s/REPLACEME/$RANDOM/g" | http POST http://127.0.0.1:5000
#else
#	cat test.json  | sed "s/REPLACEME/$RANDOM/g;s/rep2/$RANDOM/g" | http POST http://127.0.0.1:5000
#fi

echo "{\"uid\":\"$RANDOM\",\"kpairs\":["
cat little_word_list.txt | while read line;
do
	echo "{\"key\":\"$line\",\"value\":\"$RANDOM\"},"
done
echo "{\"key\":\"$line\",\"value\":\"$RANDOM\"}"
echo "]}"

#while true; do ./test.sh | http http://127.0.0.1:5000 ; done

#python -m cProfile ./entropydb.py | head -n 20 > profile.txt ; cat profile.txt

