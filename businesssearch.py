#
#SMS test via Google Voice
#
#John Nagle
#   nagle@animats.com
#
from googlevoice import Voice
from googlevoice.util import input
import sys
import BeautifulSoup
import re
import time
import pywapi
import pprint
import re
import string
from getbusiness import *
from getlocation import *

x = 1
while x > 0:
    text =  0
    
    def extractsms(htmlsms) :
        
        
        """
        extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

        Output is a list of dictionaries, one per message.
        """
        msgitems = []										# accum message items here
        #	Extract all conversations by searching for a DIV with an ID at top level.
        tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
        conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
        for conversation in conversations :
            #	For each conversation, extract each row, which is one SMS message.
            rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
            for row in rows :								# for all rows
                #	For each row, which is one message, extract all the fields.
                msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
                spans = row.findAll("span",attrs={"class" : True}, recursive=False)
                for span in spans :							# for all spans in row
                    cl = span["class"].replace('gc-message-sms-', '')
                    msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
                msgitems.append(msgitem)					# add msg dictionary to list
        return msgitems
        
    voice = Voice()
    voice.login('Enter email here', 'Enter password here')

    voice.sms()
    for msg in extractsms(voice.sms.html):
        text = str(msg)

    #print text
    if text !=0:
        textlist = re.split('\'', text)
        text = textlist[3]
        phonenumber = textlist[7]
        phonenumber = phonenumber[:-1]
        
        postal_code = re.search(r'.*(\d{5}(\-\d{4})?)$', text)
        azip =  postal_code.groups(0)
        zipcode = azip[0]
        place = text[:-6]
        print place
        print zipcode
        
        location = get_location(zipcode)
        latitude = str(location[0])
        longitude = str(location[1])
        location = latitude+','+longitude
        print location
        
        data = find_business(place, location)
        print data
        if data != "No results":
            for x in data:
                name = x[0]
                address = x[1]
                phone_number = str(x[2])
                try:
                    rating = x[3]
                except IndexError:
                    rating = 0

                #name = str(data[0])
                #address = str(data[1])
                #phone_number = str(data[2])
                #rating = data[3]
                if rating == 0:
                    string = name + '. '+address + '. ' + phone_number + '. '
                elif rating == 0 and phone_number == 0:
                    string = name + '. '+address + '. ' + '. '
                elif phone_number == 0:
                    string = name + '. '+address + '. ' + rating + '. '
                elif rating != 0:
                    rating = str(x[3])
                    string = name + '. '+address + '. ' + phone_number + '. '+rating
                else:
                    pass
                
                voice.send_sms(phonenumber, string)
        elif data == "No results":
            voice.send_sms(phonenumber, data)
        else:
            pass
            
        for message in voice.sms().messages:
            message.delete()
    else:
        pass
        
    text = 0
    print "..."
    time.sleep(25)





