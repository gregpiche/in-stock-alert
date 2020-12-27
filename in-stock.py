# Download the helper library from https://www.twilio.com/docs/python/install
import os
import requests
from twilio.rest import Client
from bs4 import BeautifulSoup

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_IN-STOCK_SID']
auth_token = os.environ['TWILIO_IN-STOCK_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Get environment var for phone numbers
personal_num = os.environ['PERSONAL_NUM']
twilio_num = os.environ['TWILIO_IN-STOCK_NUM']

item1 = "https://www.fitnessavenue.ca/265lbs-cast-iron-grip-standard-weight-plate-set-1-inch"
item2 = "https://www.fitnessavenue.ca/amstaff-df-1161a-power-squat-rack-with-lat-pull-down-attachment"
item3 = "https://www.fitnessavenue.ca/amstaff-tr057d-squat-press-rack"
item4 = "https://www.fitnessavenue.ca/heavy-duty-interlocking-foam-mat-12-pack"

page1 = requests.get(item1)
page2 = requests.get(item2)
page3 = requests.get(item3)
page4 = requests.get(item4)

#pages = [(item1, page1),(item2, page2),(item3, page3),(item4, page4)]
pages = [(item1, page1),(item2, page2),(item3, page3)]
#pages = [(item1, page1),(item2, page2)]
inStock = []

for page in pages:
    soup = BeautifulSoup(page[1].content, 'html.parser')
    hasButton = soup.find(class_="std_add_to_cart").find("button")
    if hasButton != None:
        inStock.append(page[0])

if len(inStock) == 1:
    for stock in inStock:
        message = client.messages \
                .create(
                     body=
                     "The following item is back in stock:\n• " + inStock[0],
                     from_= twilio_num,
                     to= personal_num
                     )
elif len(inStock) > 1:
    bod = "The following items are back in stock:" 
    for stock in inStock:
        bod = bod + "\n• " + stock 
    message = client.messages \
                .create(
                     body= bod,
                     from_= twilio_num,
                     to= personal_num
                     )

#print(message.sid)
#print(message)