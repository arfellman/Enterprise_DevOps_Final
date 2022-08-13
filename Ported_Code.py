#!/usr/bin/env python3
# This code makes two seperate API calls. The first uses user input data to make an API call and then writes
# the result to a file. The second makes and API and then filters the result to get the most recent Terraform
# version avialable. This Terraform version zip is then downloaded.
# A third API call has been added to this port code for a third tasks (Task #3) in the assessment. For this
# third task, we manipulate data from a third API

import requests, os.path, os


# This section create an API call to a public API with user input data and write result to file
# Function reaches out to agify API and returns a responce in json
def get_data(name):
    response = requests.get('https://api.agify.io/?name=' + str(name))
    apioutput = response.json()
#    print(apioutput)
    return apioutput

# Get users first name
user_name = input('What is your first name? ')

#Pass user first name to get_data function
result = get_data(user_name)

# The json response from get_data() is written to a file
# After adding an API call for Task #3, this seciont cas moved to the end of the script
#with open('my_agify_info.json', 'w') as file:
#    file.write(str(result))



#The next section manipulates an API call response to determine and download the most up to date TF version
tf_json = requests.get('https://releases.hashicorp.com/terraform/index.json')
tf_response = tf_json.json()

versions = tf_response['versions']
#print(versions)

URLlist = []
# The number of each version block changes, the for loop below will take any version value
for versions in versions.values():
    # The second for loop gets us to each url under builds
    for builds in versions['builds']:
        url = builds['url']
        #print(url)
        # If statement to find urls that are not rc or beta, but are linux_amd64 compatible
        #if not url.find("rc") and not url.find("beta") and url.find("linux_amd64"):
        if url.endswith("linux_amd64.zip") and not "rc" in url.lower() and not "beta" in url.lower():
            URLlist.append(url)
#print(URLlist)
latest_version = URLlist[-1]
#print(latest_version)
latest_zip = latest_version.split("/")[-1]
#print(latest_zip)

# Check if the latest TF zip has been downloaded and if not, download it
if not os.path.exists(latest_zip):
#    print("downloading")
    get_zip = requests.get(latest_version)
    with open(latest_zip, 'w') as file:
        file.write(str(get_zip))

# Clears the terminal and bids goodbye to the user
os.system('clear')
print("That's all folks!")



# This is a third API call for Task 3
# This section grabs the users IP and location and appends it to the agify json to create a record of who last  
# ran this script to grab the latest TF version

# Def gets and returns the users IP, region, and city
def get_location():
    response_location = requests.get('http://ipwho.is/')
    apioutput_location = response_location.json()
    #print(apioutput_location)
    
    city = apioutput_location['city']
    region = apioutput_location['region']
#    country = apioutput_location['country']
    user_ip_address = apioutput_location['ip']
    #print(country)
    
    return user_ip_address, region, city

result_ip, result_region, result_city = get_location()

#print('Your IP address is originating from: ' + str(result_ip) + str(result_region) + str(result_city))

# The name the user provided above (see note about this section moving from the first API call section above)
# the user IP, region, and city are all written to the agify json file
with open('my_agify_info.json', 'w') as file:
    file.write(str(result) + "\n" + "The user who last ran this script was from: " + "\n" + "IP: " + str(result_ip) + "\n" + "Region, City: " + str(result_region) + ", " + str(result_city))
