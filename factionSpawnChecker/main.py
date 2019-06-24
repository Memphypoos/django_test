import configparser
import sso
import requests
import getCharName
import ratDictionary
from datetime import datetime
import time
from requests.auth import HTTPBasicAuth

#--------------------------------------------------------------------------#
# Variables / Config Items                                                 #
#--------------------------------------------------------------------------#
config = configparser.ConfigParser()
config.read("config.ini")
eve_client = config.get("config", "eve_client")
eve_secret_key = config.get("config", "eve_secret_key")
refresh_token = config.get("config","refresh_token")
corp_id = config.get("config","corporation_id")
login_server = config.get("config", "login_server")
slack_token = config.get("config","slack_token")
slack_channel = config.get("config", "slack_channel")
scopes = config.get("config", "scopes")
authcode = config.get("config", "auth_code")
corp_id = config.get("config", "corp_id")

#--------------------------------------------------------------------------#
# FIRST TIME USE ONLY:                                                     #
# This will construct your URL based off the scopes to get the AuthCode    #
#                                                                          #
# request_callback_url = sso.constructUrl(login_server, eve_client, scopes)#
#                                                                          #
# This will take the AuthCode and exchange it for an access token, this    #
# allows you to exchange access_code for refresh_tokens                    #
#                                                                          #
# request_access_code = sso.requestAuthCode(authcode)                      #
# print(request_access_code)                                               #
#--------------------------------------------------------------------------#

#--------------------------------------------------------------------------#
# Once you have set the above up and have a refresh code, this is where the#
# Main part of the program begins                                          #
#=-------------------------------------------------------------------------#
# Variables                                                                #
#--------------------------------------------------------------------------#
big_kills = {} # array of summed kills
page = 1
npc_list = ratDictionary.delveRats

start_date = config.get("config", "start_date")
slack_message_ratting_title = '*Faction spawns since '+start_date+':* \n'
slack_message_ratting = ""
access_token = sso.refresh_esi_token(refresh_token)
header = {"User-Agent":"FactionCheckerer:Memphypoos","Authorization":"Bearer "+str(access_token)}

#--------------------------------------------------------------------------#
# Pulls API                                                                #
#                                                                          #
# Interogates the transactions in the API pull, beginning page 1           #
#--------------------------------------------------------------------------#
while page < 15:
  div_one = requests.get("https://esi.evetech.net/v3/corporations/"+str(corp_id)+"/wallets/1/journal/?page="+str(page), headers=header).json  
  if page == 15:
    break # this is the exit loop.
  for transaction in div_one():
    start_date = config.get("config", "start_date")
    date_str = transaction["date"]  # Converts each date to an object.
    if date_str[:10] >= start_date: # Splices timestamp to compare it to the start_date you

  # This will iterate through and locate each of the Ratting Transactions
      if transaction["ref_type"] == "bounty_prizes": # and transaction["reason"] not None:    
        tempItemList = transaction["reason"].split(",")
        charID = transaction["second_party_id"]

        for entry in tempItemList:
          entries = entry.split(":")
          if entries[0] in npc_list: #If we find a matching NPC type
            if not charID in big_kills: # if we can't find this character in the big_kills dict:
              big_kills[charID] = {} # Create it as a blank dict itself (to hold the type IDs and values)
            if not entries[0] in big_kills[charID]: #If we can't find this type in the char dict
              big_kills[charID][entries[0]] = 0 # Set it to 0 to start a count
            big_kills[charID][entries[0]] += int(entries[1]) # Add 1 as we have found a matching kill
  page += 1

for char in big_kills: # Get each charID from big_kills and call it char
  for type in big_kills[char]: # Get each type from big_kills[char] dict and call it type
   slack_message_ratting += (getCharName.get_char_name(char) + " killed " + str(big_kills[char][type]) + " x " + npc_list[type]+"\n")
print(slack_message_ratting_title + slack_message_ratting)

##Posting the request to Slack###
def post_to_slack(slack_message_ratting):
  header2 = {'User-Agent':"slack:Github\Memphypoos",'Authorization':'Bearer '+str(slack_token), 'Content-Type': "application/json; charset=utf-8"}
  slack = requests.post("https://slack.com/api/chat.postMessage", headers=header2, json=({'channel' : slack_channel, 'text': slack_message_ratting, 'as_user': 'true'}))
  print("Request posted to slack")
post_to_slack(slack_message_ratting_title + slack_message_ratting) 
