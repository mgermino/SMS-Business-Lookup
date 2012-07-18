import urllib2
import simplejson
import time
# The request also includes the userip parameter which provides the end
# user's IP address. Doing so will help distinguish this legitimate
# server-side traffic from traffic which doesn't come from an end-user.
API_key = 'AIzaSyB8AgPKlO0PURl7ScWmxI9A8V8DsVJIcF4'

#finds the business using google's places API and returns the data to main
def find_business(name, location):
    x = 0
    outsidelist = []
    
    print'---------------------------'
    print name
    print location
    name = name.replace (" ", "+")
        
    url = ('https://maps.googleapis.com/maps/api/place/search/json?location='+location+'&radius=10000&name='+name+'&sensor=false&key='+API_key)
    request = urllib2.Request(
        url, None, {'Referer': 'http://www.google.com'})
    response = urllib2.urlopen(request)
    # Process the JSON string.
    results = simplejson.load(response)
    print results
    if results['status'] == 'OK':
        while x < 3:
            insidelist = []
            url = ('https://maps.googleapis.com/maps/api/place/search/json?location='+location+'&radius=10000&name='+name+'&sensor=false&key='+API_key)
            request = urllib2.Request(
                url, None, {'Referer': 'http://www.google.com'})
            response = urllib2.urlopen(request)

            # Process the JSON string.
            results = simplejson.load(response)
            referenceID =  results['results'][x]['reference']
            print referenceID

            
            url = ('https://maps.googleapis.com/maps/api/place/details/json?reference='+referenceID+'&sensor=true&key='+API_key)

            request = urllib2.Request(
                url, None, {'Referer': 'http://www.google.com'})
            response = urllib2.urlopen(request)

            # Process the JSON string.
            results = simplejson.load(response)


            address =  results['result']['formatted_address']
            try:
                phone_number = results['result']['formatted_phone_number']
            except KeyError:
                pass
            place = results['result']['name']
            var = str(x)
            try:
                rating = results['result']['rating']
                rating = 'Rating: '+str(rating)
                insidelist.append(place)
                insidelist.append(address)
                try:
                    insidelist.append(phone_number)
                except UnboundLocalError:
                    pass
                insidelist.append(rating)
                outsidelist.append(insidelist)
            except KeyError:
                rating = 0
                insidelist.append(place)
                insidelist.append(address)
                try:
                    insidelist.append(phone_number)
                except UnboundLocalError:
                    pass
                insidelist.append(rating)
                outsidelist.append(insidelist)
            
            print '-----------------'
            x+=1
        return outsidelist

    elif results['status'] == 'ZERO_RESULTS':
        zero =  "No results"
        return zero
    else:
        return 0
