#!/bin/bash

echo -e "FUZZING PORT 8001\n"
python3 buzzshock.py -e http://localhost:8001 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 1

echo -e "FUZZING PORT 8002\n"
python3 buzzshock.py -e http://localhost:8002 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 1

echo -e "FUZZING PORT 8003\n"
python3 buzzshock.py -e http://localhost:8003 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 1

echo -e "FUZZING PORT 8004\n"
python3 buzzshock.py -e http://localhost:8004 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 1

echo -e "FUZZING PORT 8005\n"
python3 buzzshock.py -e http://localhost:8005 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 1

echo -e "FUZZING PORT 8006\n"
python3 buzzshock.py -e http://localhost:8006 -pl HttpLaxClPlugin,HttpLaxTePlugin,HttpVersionPlugin -el HttpBuzzEngine -pt http -t 1
