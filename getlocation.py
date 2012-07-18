from getbusiness import*
from googlemaps import GoogleMaps


#Gets your location (lat/long) based on your zip code
def get_location(zipcode):
    
    gmaps = GoogleMaps(API_key)

    latlong = gmaps.address_to_latlng(zipcode)

    return latlong


