#--------------------------------------------------------------------------#
# To Do List:                                                              #
# 1) Sort the results by highest amount                                    #
#--------------------------------------------------------------------------#
import configparser
import sso
import requests
import getCharName
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
tax = config.get("config", "tax_rate")
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
#--------------------------------------------------------------------------#

#--------------------------------------------------------------------------#
# This will take the AuthCode and exchange it for an access token, this    #
# allows you to exchange access_code for refresh_tokens                    #
#                                                                          #
# request_access_code = sso.requestAuthCode(authcode)                      #
# print(request_access_code)                                               #
#--------------------------------------------------------------------------#

#--------------------------------------------------------------------------#
# Once you have set the above up and have a refresh code, this is where the#
# Main part of the program begins                                          #
#--------------------------------------------------------------------------#
ratting = 0 # ratting bounty_prizes
char_ratting = {} # array of characters
page = 1
start_date = config.get("config", "start_date")
slack_message_ratting_title = '*Total Pirate Bounty Rewards since '+start_date+':* \n'
slack_message_ratting = ""
access_token = sso.refresh_esi_token(refresh_token)
header = {"User-Agent":"WalletAudit:Memphypoos","Authorization":"Bearer "+str(access_token)}

#--------------------------------------------------------------------------#
# This will retrieve data from each of the pages of the Wallet API.
#--------------------------------------------------------------------------#
while page < 3:
  div_one = requests.get("https://esi.evetech.net/v3/corporations/"+str(corp_id)+"/wallets/1/journal/?page="+str(page), headers=header).json
  if page == 3:
    break
  for transaction in div_one():
    start_date = config.get("config", "start_date")
    date_str = transaction["date"]  # Converts each date to an object.
    if date_str[:10] >= start_date: # Splices timestamp to compare it to the start_date you want
  # This will iterate through and locate each of the Ratting Transactions
      if transaction["ref_type"] == "bounty_prizes" and transaction["amount"] > 0:
        ratting += transaction["amount"]
        # Figure out what this is doing......
        if not transaction["second_party_id"] in char_ratting:
          char_ratting[transaction["second_party_id"]] = 0 
        char_ratting[transaction["second_party_id"]] += transaction["amount"]
  page += 1
  print("Page: "+str(page))

#------------------------------------------------------------------------------#
# This constructs the message and does the math to extrapolate the full amount
#------------------------------------------------------------------------------#
for character in char_ratting:
  val100 = (char_ratting[character] * 100 / int(tax)) #comment out before the * to see tax only
  slack_message_ratting += getCharName.get_char_name(character)+" ratted "+str("{:,.2f}".format(val100))+" ISK"+"\n"
print(slack_message_ratting)

##Posting the request to Slack###
def post_to_slack(slack_message_ratting):
  header2 = {'User-Agent':"slack:Github\Memphypoos",'Authorization':'Bearer '+str(slack_token), 'Content-Type': "application/json; charset=utf-8"}
  slack = requests.post("https://slack.com/api/chat.postMessage", headers=header2, json=({'channel' : slack_channel, 'text': slack_message_ratting, 'as_user': 'true'}))
  print("Request posted to slack")
post_to_slack(slack_message_ratting_title + slack_message_ratting) #is is all
#post_to_slack(slack_message_ratting_title2 + slack_message_ratting) #this is tax only
