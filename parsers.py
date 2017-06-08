#!/usr/bin/env python3


def check_xml(word):
    if (word is not None) and (str(word) is not "None"):
        # word = str(word.text)
        word = word
    else:
        word = ""

    return word


def check_json(word):
    if (word is not None) and (str(word) != "None"):
        pass
    else:
        word = ""
    return word


def write_hotel_data(file, hotelId, provider_name, giata_id, name, address, description, city,
                     provider_city_id, destination, provider_destination_id, country, country_iso_code,
                     zipcode, rating, facilities, latitude, longitude):  # def write_hotel_data(file, hotelId, name, description, address, rating, facilities, city, country, zipcode, latitude, longitude, state):
    data_dict = {"hotelId": hotelId,
                 "provider_name": provider_name,
                 "giata_id": giata_id,
                 "name": name,
                 "address": address,
                 "description": description,
                 "city": city,
                 "provider_city_id": provider_city_id,
                 "destination": destination,
                 "provider_destination_id": provider_destination_id,
                 "country": country,
                 "country_iso_code": country_iso_code,
                 "zipcode": zipcode,
                 "rating": rating,
                 "facilities": facilities,
                 "latitude": latitude,
                 "longitude": longitude
                 }

    file.writerow(data_dict)


def write_image_data(file, hotelId, provider_name, url, image_text, default, size):  # def write_image_data(file, hotelId, url, image_text, default, size): # file_object, hotel Id, full url, image_text/ qualifier, default: 'Y' or '' , size: 'S,R,L' for small, regular, large
    data_dict = {"hotelId": hotelId,
                 "provider_name": provider_name,
                 "full_url": url,
                 "image_text": image_text,
                 "default": default,
                 "size": size
                 }

    file.writerow(data_dict)