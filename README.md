# loxoneUUIDextract
Automation of UUID extraction for Loxone Miniserver in combination with https://github.com/andrasg/loxone-influx
This python script automates the UUID extraction and generats a config file.

## Extraction of UUIDs
All uuids which are set up for internal statistics of Loxone software are extracted. 

## Configuration
Same config file format is used for input and output. Credentials of Loxone Miniserver are used to fetch json file. 

## Future
Plan is to have a docker container which can be run periodically. 
