#!/bin/bash

echo "Waiting for influxdb..."

while ! nc -z localhost 8086; do
  sleep 0.1
done

echo "influxdb started, initializing setup:"

influx setup -u $INFLUX_USER -b $INFLUX_BUCKET_NAME -p $INFLUX_PSW -t $INFLUX_TOKEN -r $INFLUX_RETENTION_TIME -o $INFLUX_ORG -f
