#!/bin/bash

echo -e "FUZZING PORT 9001\n"
python3 buzzshock.py -e http://localhost:9001 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 8 

echo -e "FUZZING PORT 9002\n"
python3 buzzshock.py -e http://localhost:9002 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 8

echo -e "FUZZING PORT 9003\n"
python3 buzzshock.py -e http://localhost:9003 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 8
echo -e "FUZZING PORT 9004\n"
python3 buzzshock.py -e http://localhost:9004 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 8

echo -e "FUZZING PORT 9005\n"
python3 buzzshock.py -e http://localhost:9005 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 8

echo -e "FUZZING PORT 9006\n"
# python3 buzzshock.py -e http://localhost:9006 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 8
