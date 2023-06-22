import requests
import json
import os
from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv()

# Download the helper library from https://www.twilio.com/docs/python/install

account_sid = os.getenv('ACCOUNT_SID') #Account SID comes from own Twilio API account.
auth_token = os.getenv('AUTH_TOKEN') #Auth Token comes from own Twilio API account.
client = Client(account_sid, auth_token) #Creating a valid Twilio client after verifying SID and Auth_Token.

itemID = ["Giggle_Bundle", "EID_AutumnTea","Character_FallValleyCharge", "Character_FallValleyBlink", "CID_A_222_Athena_Commando_F_Relish_G6S5T", "CID_A_295_Athena_Commando_M_RustyBolt_FEHJ0", "CID_971_Athena_Commando_M_Jupiter_S0Z6M", "CID_964_Athena_Commando_M_Historian_869BC", "Character_FearlessFlightMenace", "CID_A_358_Athena_Commando_F_Lurk", "CID_A_204_Athena_Commando_M_ClashV_SQNVJ", "CID_736_Athena_Commando_F_DonutDish", "Character_SwampKnight", "EID_Heartsign", "EID_Haste1_T98Z9", "EID_Comrade_6O5AK", "EID_Suspenders", "EID_Downward_8GZUA", "EID_HotPink", "EID_NeverGonna", "EID_Tidy", "EID_TrueLove", "EID_KissKiss"] #List of fornite skin/emote IDs. Those can be found at this site: https://fortnite.gg/cosmetics
typeID = ["Emote", "Outfit", "Item Bundle", "4 Item Bundle", "5 Item Bundle"] # List of filters to help find specific cosmetic types.
flag = False # Boolean flag to check for item availability, initially set to false.

url = "https://fortniteapi.io/v2/shop?lang=en" # Specific API call url.

payload = {}
headers = {
  'Authorization': os.getenv('APIKEY'), # Using API key for authorization.
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)
data = response.json()["shop"] # Focusing on the 'shop' aspect of the response.
resultList = [] # Empty list for storing results, if any, for formatting later.

for shopDict in data:  
    if shopDict["displayType"] in typeID and shopDict["mainId"] in itemID: # If shop items match the filter (aka a skin or emote) and an item ID also matches the IDs from my personal list.
        flag = True
        resultList.append(shopDict["displayName"])
        print(shopDict["displayName"])

if not flag:
    message = client.messages.create(
        body= "Nothing from your list is available in the Fortnite shop today.",
        from_= os.getenv('FROMNUM'), # This variable holds the number that Twilio services provides.
        to=os.getenv('TONUM') # Personal number.
      )
    print("No matches found today.")

else:
    result = ""
    for name in resultList:
        if resultList.index(name) == len(resultList) - 1:
          result += name + " "
        else:
          result += name + ", "  
    result += "is/are in the shop today!"
    message = client.messages.create(
            body = result,
            from_= os.getenv('FROMNUM'),
            to = os.getenv('TONUM')
          )