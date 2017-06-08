#!/usr/bin/env python3
import glob
import sys
import re
import csv
import traceback
import xmltodict
import os

from parsers import check_xml, write_hotel_data, write_image_data


def hoojoozat_details(location, output_dir, error_collector):
    
    csvfile = open(output_dir + "/hotel_info_hoojoozat.csv", 'w')
    writer = csv.writer(csvfile)
                
    t_files = glob.glob(location + "/hotel_125667.xml")

    # t_files = glob.glob(location + "/hotel_*.xml")

    # print("Total files are:", len(t_files))

    for file in t_files:
        try:
            with open(file) as fd:
                doc = xmltodict.parse(fd.read())
            # print(doc)
                
            giata_id = ""
                    
            provider_name = "hoojoozat"

            country_iso = ""

            facilities = ""
                
            try:
                hotel_id = doc['string']['HotelDetail']['HotelDetails']['Code']

                print(hotel_id)

                name = check_xml(doc['string']['HotelDetail']['HotelDetails']['Name'])

                print(type(name))

                address = check_xml(doc['string']['HotelDetail']['HotelDetails']['Address'])

                description = check_xml(doc['string']['HotelDetail']['HotelDetails']['Description'])

                city = check_xml(doc['string']['HotelDetail']['HotelDetails']['Destination'])

                provider_city_id = ""

                destination = check_xml(doc['string']['HotelDetail']['HotelDetails']['Zone'])

                provider_destination_id = ""

                country = check_xml(doc['string']['HotelDetail']['HotelDetails']['Country'])

                postal_code = check_xml(doc['string']['HotelDetail']['HotelDetails']['PostalCode'])

                star_rating = check_xml(doc['string']['HotelDetail']['HotelDetails']['Category'])
                for category in star_rating:
                    match = re.match("^[0-9]\.?[0-9]?", category)
                    if match:
                        category

                latitude = check_xml(doc['string']['HotelDetail']['HotelDetails']['Latitude'])

                longitude = check_xml(doc['string']['HotelDetail']['HotelDetails']['Longitude'])

                writer.writerow([hotel_id, provider_name, giata_id, name, address, description, city,
                                provider_city_id, destination, provider_destination_id, country,
                                country_iso, postal_code, category, facilities, latitude, longitude])

            except Exception as e:
                print(traceback.format_exc())
                tb = sys.exc_info()[2]
                error_collector.write("\nFailed at Line %i " % tb.tb_lineno)
                error_collector.write("\nError: {0}, HotelID: {1}".format(str(e), hotel_id))
                continue
        except Exception as e:
            print(e)

    csvfile.close()


# def hoojoozat_images(location, output_dir, error_collector):

#     # hotelId, provider_name, url, image_text, default, size

#     csvfile = open(output_dir + "/hotel_info_hoojoozat_images.csv", 'w')
#     writer = csv.writer(csvfile)
                
#     t_files = glob.glob(location + "/hotel_125667.xml")

#     # print("Total files are:", len(t_files))
#     for file in t_files:
#         try:
#             with open(file) as fd:
#                 doc = xmltodict.parse(fd.read())
#              try:
#                 hotel_id = doc['string']['HotelDetail']['HotelDetails']['Code']

#                 print(hotel_id)

#                 provider_name = "hoojoozat"

#                 url = check_xmal(doc['string']['HotelDetail']['HotelDetails']['Website'])

#                 image_text = ""

#                 default = ""

#                 size = ""

#                 writer.writerow([hotel_id, provider_name, url, image_text, default, size])

#             except Exception as e:
#                 print(traceback.format_exc())
#                 tb = sys.exc_info()[2]
#                 error_collector.write("\nFailed at Line %i " % tb.tb_lineno)
#                 error_collector.write("\nError: {0}, HotelID: {1}".format(str(e), hotel_id))
#                 continue
#         except Exception as e:
#             print(e)

#     csvfile.close()



if __name__ == "__main__":
    error_collector = open("Error_happened_hoojoozat", 'w')
    # files_location = sys.argv[1]
    # output_dir = sys.argv[2]

    cwd = os.path.dirname(os.path.abspath(__file__))
    
    files_location = cwd + '/hoojoozat/hotel_info/'

    output_dir = cwd + '/hoojoozat/csv_file/'

    os.makedirs(output_dir, exist_ok = True)

    print(">>hoojoozat")
    error_collector.write("\n>>hoojoozat\n")
    print("Getting hotel details..")
    error_collector.write("\nGetting hotel details..")
    hoojoozat_details(files_location, output_dir, error_collector)
    # print("Getting hotel images..")
    # error_collector.write("\nGetting hotel images..")
    # hoojoozat_images(files_location, output_dir, error_collector)

    error_collector.close()



# python3 hoojoozat_parser_1.py 


# hotel_id, provider_name, giata_id, name, address, description, city,provider_city_id, destination, provider_destination_id, country,country_iso, postal_code, category, facilities, latitude, longitude