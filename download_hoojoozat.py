import os
import xml.etree.ElementTree as ET
import glob
import sys
import requests


def get_hotel_info(username, password, output_dir_hotel_info, error):
	
	error_hotelcodes = open(error + '/failed_hotelcodes.txt', 'w')

	file_error = open(error + "/file_error.txt", 'w')

	files = glob.glob(output_dir_hotels_list + 'hotel_*.xml')

	# files = [output_dir_hotels_list + '/hotel_15257.xml']
	
	# print(files)
	
	print("Total files in hotels_list", len(files))
	
	hotel_codes = []

	for file in files:

		print("cursor is at file:", file, 'at index', files.index(file))
		
		try:
			tree = ET.parse(file)
		
			root = tree.getroot()
		
			ns = {'string': 'http://hoojoozat.com/', 'HotelsList': 'http://tempuri.org/HotelList.xsd'}
		
			for hotel in root.find("HotelsList:HotelsList",ns).findall("HotelsList:Hotel", ns):
		
				hotel_code = hotel.find('HotelsList:Code',ns)
		
				hotel_code = hotel_code.text
		
				# print(hotel_code)
		
				hotel_codes.append(hotel_code)
		
				# print(hotel_codes)
		
			print("Total hotelcodes:", len(hotel_codes))

			# hotel_codes = ['99999000000000', '58099','383083']

			
			for i in hotel_codes:
			
				print("Sending request for hotel code", i, 'at index', hotel_codes.index(i))
			
				try:
					url = "http://130.211.25.226/hotelservices.asmx/GetHotelDetails"

					querystring = {"AgentUsername":"amantravels","AgentPassword":"aman2017","HotelCode":i}

					headers = {
					    'content-type': "text/xml",
					    'soapaction': "GetHotelDetails",
					    'cache-control': "no-cache",
					    'postman-token': "200e0096-a258-bd9b-bec1-d9e63a13c322"
					    }
					 
					response = requests.request("GET", url, headers=headers, params=querystring)
					# print(response.text)
					hotelinfo_response = format(response)
					# print(hotelinfo_response, i)
					
					root = ET.fromstring(hotelinfo_response)
					# print(root)
					ns = {'string': 'http://hoojoozat.com/', 'HotelDetail': 'http://tempuri.org/HotelDetail.xsd'}
					
					for hotel in root.find("HotelDetail:HotelDetail",ns).findall("HotelDetail:HotelDetails", ns):
						
						hotel_id = hotel.find('HotelDetail:Code',ns)
						
						hotel_id = hotel_id.text
						
						print(hotel_id)	
						
						if hotel_id:
							with open(output_dir_hotel_info + 'hotel_' + i + '.xml', 'w') as wobj:
								wobj.write(hotelinfo_response)

					error = root.find("HotelDetail:HotelDetail",ns).find('HotelDetail:Error', ns)
					
					# print(error)
					
					if error is not None:
						raise Exception("Exception raised while downloading hotel info")
					
				except Exception as e:
					error_hotelcodes.write(str(sys.exc_info()[0]) + '\n')
					
					error_hotelcodes.write(str(e) + 'hotel_' + i + '.xml' + '\n')
		
		except Exception as e:
			file_error.write(str(e) + '\n')

			file_error.write("Error happended with file: " + file + '\n')

	error_hotelcodes.close()

	file_error.close()


def get_hotels_list(username, password, output_dir_hotels_list, error):
	
	file_error = open(error + "/file_error.txt", 'w')

	error_destinations = open(error + '/failed_destinations.txt', 'w')

	destination_codes = []

	files = glob.glob(output_dir_hotels_list + '/hotel_*.xml')

	# files = [output_dir_dest + '/hotel_425.xml']

	print("Total destination codes:", len(files))
	
	for file in files:

		print("cursor is at file:", file, files.index(file))
		
		try:
			tree = ET.parse(file)
		
			root = tree.getroot()
			# print(root)
		
			ns = {'string': 'http://hoojoozat.com/', 'Destinations': 'http://tempuri.org/Destination.xsd'}
		
			for destination in root.find("Destinations:Destinations",ns).findall("Destinations:Destination", ns):
				
				destination_code = destination.find('Destinations:Code',ns)
				
				destination_code = destination_code.text
				
				# print(destination_code)

				destination_codes.append(destination_code)
				
				# print(destination_codes, "dest codes list")
			# destination_codes = ['89800000000000000000000','15257']

			print("Total destination codes:", len(destination_codes))
			

			for i in destination_codes:

				print("sending request for destination code:", i, 'at index', destination_codes.index(i))

				try:
					
					url = "http://130.211.25.226/hotelservices.asmx/GetHotelList"

					querystring = {"AgentUsername":"amantravels","AgentPassword":"aman2017","DestinationCode":i}

					headers = {
				    	'content-type': "text/xml",
				    	'soapaction': "GetHotelList",
				    	'cache-control': "no-cache",
				    	'postman-token': "e161faae-cf16-aaf2-7be3-26a63cd5249e"
				    	}

							
					response = requests.request("GET", url, headers=headers, params=querystring)

					hotelslist_response = format(response)

					# print(hotelslist_response)

					root = ET.fromstring(hotelslist_response)

					ns = {'string': 'http://hoojoozat.com/', 'HotelsList': 'http://tempuri.org/HotelList.xsd'}
	
					for hotel in root.find("HotelsList:HotelsList",ns).findall("HotelsList:Hotel", ns):
		
						hotel_code = hotel.find('HotelsList:Code',ns)
		
						hotel_code = hotel_code.text
		
						# print(hotel_code)

						if hotel_code:
							with open(output_dir_hotels_list + 'hotel_' + i + '.xml', 'w') as wobj:
								wobj.write(hotelslist_response)

					error = root.find("HotelsList:HotelsList",ns).find('HotelsList:Error', ns)
					# print(error)

					if error is not None:
						raise Exception("Exception raised while downloading destinationcode.xml ")

				except Exception as e:		
					error_destinations.write(str(sys.exc_info()[0]) + str(e) + ' hotel_destination_' + i + '\n')
						
		except:
			file_error.write(str(sys.exc_info()[0]) + str(e) + '\n')

			file_error.write("Error happended with file: " + file + '\n')

	
	error_destinations.close()
	
	file_error.close()
			
	

def get_destinations(username, password, output_dir_dest, error):

	error_countries = open(error + '/failed_countries.txt', 'w')
		
	countries = []

	file = output_dir + "hotel_countries.xml"

	tree = ET.parse(file)

	root = tree.getroot()

	ns = {'string': 'http://hoojoozat.com/', 'Countries': 'http://tempuri.org/XMLSchema.xsd'}

	for country in root.find("Countries:Countries",ns).findall("Countries:Country", ns):
		
		code = country.find('Countries:Code',ns)
		
		country_code = code.text
		
		countries.append(country_code)

	print("Total countries:", len(countries))

	
	for i in countries:

		print("sending request to download country:", i, "at index", countries.index(i))

		try:
			url = "http://130.211.25.226/hotelservices.asmx/GetDestinations"

			querystring = {"AgentUsername":"amantravels","AgentPassword":"aman2017","CountryCode":i}

			headers = {
	    		'content-type': "text/xml",
	    		'soapaction': "GetDestinations",
	    		'cache-control': "no-cache",
	    		'postman-token': "4434a904-51cc-e271-a256-b9e3008304f5"
	    		}
		
			response = requests.request("GET", url, headers = headers, params = querystring)

			dest_response = format(response)
			# print(response.text)
			root = ET.fromstring(dest_response)
			# print(root)
			ns = {'string': 'http://hoojoozat.com/', 'Destinations': 'http://tempuri.org/Destination.xsd'}

			for destination in root.find("Destinations:Destinations",ns).findall("Destinations:Destination", ns):
				
				destination_code = destination.find('Destinations:Code',ns)
				
				destination_code = destination_code.text

				if destination_code:
					with open(output_dir_dest + '/hotel_' + i + '.xml', 'w') as wobj:
						wobj.write(dest_response)

			error = root.find("Destinations:Destinations",ns).find("Destinations:Destination", ns)
			print(error)

			if error is not None:
				raise Exception("Exception raised while downloading countries")

		# except requests.exceptions.Timeout as to:
			# error_countries.write("Error : hotel_" + i + '.xml' + ' ' + str(to) + '\n')
		# except IOError as io:
			# error_countries.write("Error : hotel_" + i + '.xml' + ' ' + str(io) + '\n')
		except Exception as e:	    
		    error_countries.write(str(sys.exc_info()[0]) + str(e) + 'hotel_country_' + i + '.xml' + '\n')
		    
	error_countries.close()


def get_countries(username, password, output_dir):
	
	try:
		url = "http://130.211.25.226/hotelservices.asmx/GetCountries"

		querystring = {"AgentUsername":"amantravels","AgentPassword":"aman2017"}

		headers = {
		    'content-type': "text/xml",
		    'cache-control': "no-cache",
		    'postman-token': "0e8555ad-59ef-a9c9-a7dc-74cb526430dc"
		    }
		response = requests.request("GET", url, headers=headers, params=querystring)
			
		country_response = format(response)

		root = ET.fromstring(country_response)

		# print(root)

		ns = {'string': 'http://hoojoozat.com/', 'Countries': 'http://tempuri.org/XMLSchema.xsd'}

		for country in root.find("Countries:Countries",ns).findall("Countries:Country", ns):
			
			code = country.find('Countries:Code',ns)
			
			country_code = code.text

			if country_code:
				with open(output_dir + 'hotel_countries' + '.xml', 'w') as wobj:
					wobj.write(country_response)
	
	except Exception as e:
		print("Exception occured while downloading countries.xml", str(e))
	

def format(response):
	res = response.text
	res1 = res.replace('&lt;', '<')
	res2 = res1.replace('&gt;','>')
	return res2

	
if __name__ == '__main__':
    cwd = os.path.dirname(os.path.abspath(__file__))
    output_dir = cwd + '/hoojoozat/countries/'
    print(output_dir)
    # os.system('rm -rf ' + output_dir)
    os.makedirs(output_dir, exist_ok = True)

    output_dir_dest = cwd + '/hoojoozat/destination/'
    print(output_dir_dest)
    # # os.system('rm -rf ' + output_dir_dest)
    os.makedirs(output_dir_dest, exist_ok = True)

    output_dir_hotels_list = cwd + '/hoojoozat/hotels_list/'
    print(output_dir_hotels_list)
    os.makedirs(output_dir_hotels_list, exist_ok = True)

    output_dir_hotel_info = cwd + '/hoojoozat/hotel_info/'
    print(output_dir_hotel_info)
    os.makedirs(output_dir_hotel_info, exist_ok = True)


    username = "239EBZ"
    password = "200316ZB22"

    error = cwd + '/hoojoozat/errors/'  
    os.makedirs(error, exist_ok = True)
     

    get_countries(username, password, output_dir)

    get_destinations(username, password, output_dir_dest, error)
    
    get_hotels_list(username, password, output_dir_hotels_list, error)

    get_hotel_info(username, password, output_dir_hotel_info, error)

    


