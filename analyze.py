# geo_location_maps.py


import sys
import json
import csv

import utils as utils


def tokenize(tweet):
    """
    Cleans and tokenizes the tweets
    filter out the mentions, hashtags, punctuations and
    language specific stop words.

    :param tweet: the tweet object
    :return: the cleaned and parsed terms in the given tweet's text
    """
    return utils.get_text_normalized(tweet)



def update_co_occurrence_matrix(terms, com):
    """
    Update the passed com[co-occurrence matrix] for the given terms

      - we don’t want to count the same term pair twice, e.g. com[A][B] == com[B][A],
        so the inner for loop starts from i+1 in order to build a triangular matrix.

      - 'sorted' will preserve the alphabetical order of the terms.

    :param terms: list of terms
    :param com: the co-occurrence matrix
    """
    for i in range(len(terms) - 1):
        for j in range(i + 1, len(terms)):
            w1, w2 = sorted([terms[i], terms[j]])
            if w1 != w2:
                com[w1][w2] += 1


def read_cities_data(file_path):
    """
    Reads the CSV file containing cities data

    :param file_path: the path to file containing cities data
    :return: the dictionary containing city-name as key and
             latitude & longitude as value
    """
    cities = {}
    # with open(file_path) as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         cities[row['city'].lower()] = {'lat': row['lat'], 'lng': row['lng']}
    with open(file_path) as file:

        for row in file:
            row_data = row.split('\t')
            alternatenames = list(filter(lambda v: len(v) > 3, row_data[3].split(',')))
            geo_point = {'lat': row_data[4], 'lng': row_data[5]}

            # setting geo point for the name of the location
            # ony if it's a good name,
            # as with the analysis it is found that the
            # city names with length greater than 3 are good names
            if len(row_data[1]) >= 3:
                cities[row_data[2]] = geo_point

            for alt_name in alternatenames:
                cities[alt_name.strip()] = geo_point

    return cities


def find_geo_coordinates(cities: dict, location: str):
    """
    It finds the best matched city and returns the geo-coordinates
    of that matched city.

    :param cities: the cities data which actually a dictionary
                   contains city-name as key and geo-data as value
    :param location: the user location from which we want to extract
                     the city information
    :return: the geo information having format [longitude, latitude]
    """
    coordinates = []
    # user_loc:str = location.lower()
    user_loc:str = location
    best_match = ''

    for city in cities.keys():
        if city in user_loc or city.lower() in user_loc:
            if len(city) > len(best_match):
                best_match = city
                coordinates = [cities[city]['lng'], cities[city]['lat']]

    if len(best_match) > 0:
        print("[INFO] [ %s ]  city found in user location [ %s ]" % (best_match, user_loc))
    else:
        print("[WARNING] no city found in user location [ %s ]" % (user_loc))

    return coordinates


def prepare_geo_location_data(fin, cities_data_file_path, analyze_unique_users, fout):
    """
    It reads tweets in the given file, reads the co-ordinates data of each tweet.

    :param fin: the path to the file containing tweets
    :param cities_data_file_path the file containing cities info
    :param analyze_unique_users the indicator which show whether to analyze unique users only or all
    :param fout the path to the file containing geo-location data for visualization
    :return: the geo_location data
    """
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }

    unique_users = set()
    points_added = 0
    cities_data = read_cities_data(cities_data_file_path)

    # Reads tweets from the file [fin] in which each line is a tweet as json-document
    with open(fin, 'r') as f:
        for line in f:
            # loads line as Python dictionary
            line = line.strip()
            if len(line) > 0 and line.startswith("{") and line.endswith("}"):
                tweet = json.loads(line)
                if 'coordinates' in tweet and tweet['coordinates']:
                    points_added += 1;
                    geo_json_feature = {
                        "type": "Feature",
                        "geometry": tweet['coordinates'],
                        "properties": {
                            "text": tweet['text'],
                            "created_at": tweet['created_at'],
                            "language": tweet['lang']
                        }
                    }
                    geo_data['features'].append(geo_json_feature)

                # we have user's location,
                # so try to extract the city and find the co-ordinates
                elif 'user' in tweet and 'location' in tweet['user'] and tweet['user']['location']:
                    user_id_str = tweet['user']['id_str']
                    location = tweet['user']['location']
                    coordinates = find_geo_coordinates(cities_data, location)
                    if (analyze_unique_users and user_id_str not in unique_users) or not analyze_unique_users:
                        unique_users.add(user_id_str)
                        if coordinates and len(coordinates) == 2:
                            points_added += 1
                            geo_json_feature = {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": coordinates
                                },
                                "properties": {
                                    "text": tweet['text'],
                                    "created_at": tweet['created_at'] or '',
                                    "language": tweet['lang'] or ''
                                }
                            }
                            geo_data['features'].append(geo_json_feature)


                # after every newly added 1000 points,
                #  write geo-data to file for evolution of visualization
                if points_added == 1000:
                    points_added = 0
                    write_geo_data_in_file(fout, geo_data)
                    print("[INFO] 1000 new points are added."
                          " Refresh the visualization page to see the change!")

    return geo_data



def write_geo_data_in_file(fout, geo_data):
    """
    It dumps the geo_data which contains geo location info of tweets,
    in the form of pretty json at the given path [fout]

    :param fout: the path to the file where data dump created
    :param geo_data: the geo location data of tweets that needs to be dumped
    :return: void
    """
    with open(fout, 'w') as fo:
        fo.write(json.dumps(geo_data, indent=4))


if __name__ == "__main__":
    # fname = 'data/tweets.jsonl'
    fin = 'data/stream_.jsonl'
    fout = 'visualization/geo_location_data.json'

    # cities_data_file_path = 'data/worldcities-basic_data.csv'
    cities_data_file_path = 'data/cities1000.txt'

    analyze_unique_users = False

    if len(sys.argv) == 2 and sys.argv[1] == 'unique':
        print("Analyzing Unique")
        print("================\n\n\n")
        analyze_unique_users = True

    # prepared the geo data
    geo_data = prepare_geo_location_data(fin, cities_data_file_path, analyze_unique_users, fout)

    # dumps the geo data
    write_geo_data_in_file(fout, geo_data)
