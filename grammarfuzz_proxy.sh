#!/bin/bash

echo -e "FUZZING PORT 9001\n"
python3 buzzshock.py -e http://localhost:9001 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 9002\n"
python3 buzzshock.py -e http://localhost:9002 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 9003\n"
python3 buzzshock.py -e http://localhost:9003 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 9004\n"
python3 buzzshock.py -e http://localhost:9004 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 9005\n"
python3 buzzshock.py -e http://localhost:9005 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 9006\n"
# python3 buzzshock.py -e http://localhost:9006 -pt http -gf http-abnf.txt -mtc 100000  -t 5 
