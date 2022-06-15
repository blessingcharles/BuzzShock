#!/bin/bash

sudo docker stop $(sudo docker ps -a -f status=running -q)