#!/bin/sh

cd /home/sea/Projects/DoubanBookSpider

docker-compose down

echo "Sleep 10 second"

sleep 10s

docker-compose up -d
