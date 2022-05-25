#!/bin/bash

# echo -e "FUZZING PORT 8001\n"
# python3 buzzshock.py -e http://localhost:8001 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

# echo -e "FUZZING PORT 8002\n"
# python3 buzzshock.py -e http://localhost:8002 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 8003\n"
python3 buzzshock.py -e http://localhost:8003 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 8004\n"
python3 buzzshock.py -e http://localhost:8004 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 8005\n"
python3 buzzshock.py -e http://localhost:8005 -pt http -gf http-abnf.txt -mtc 100000  -t 5 

echo -e "FUZZING PORT 8006\n"
python3 buzzshock.py -e http://localhost:8006 -pt http -gf http-abnf.txt -mtc 100000  -t 5 
