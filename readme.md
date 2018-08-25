# Geo Location Analysis

It analyze the tweets and shows the location of tweets in an interactive MAP.
Put tweets file in 'geo_location_analysis/data' folder.

## Install dependencies
Python3 is pre-requisite to this program.
There are some open-source python libraries used, which are listed in requirements.txt file.
YOu can install those packages by running `pip3 install -r requirements.txt`.


## Prepare Visualization Data
For visualization, first you have to analyze and prepare a JSON file with a specific format and
it contains the geo location related info such as co-ordinates etc.
Run following command to prepare that data.

`python3 analyze.py`<br /><br />
`python3 analyze.py unique`<br /><br />

This program creates the json file 'geo_location_data.json' at 'geo_location_analysis/visualization' path.
1st command will analyze all users and the 2nd commnd with an argument with value 'unique' will only analyze unique users.

## Run Server for Visualization
Open another terminal/command-prompt in path 'geo_location_analysis/visualization'.
Run `python -m http.server 8888` which will start an http-server on port 8888.

## Open Browser and See Chart
Open browser and goto `localhost:8888`


## Cities Info
File 'data/cities1000.txt' contains the info for more 127,000 cities.
Each row contains some specific infos which are separated by tabs and explained below.

The main table has the following fields :
---------------------------------------------------
geonameid         : integer id of record in geonames database
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int)
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format
