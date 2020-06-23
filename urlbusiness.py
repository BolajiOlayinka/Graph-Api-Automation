import requests
import json

my_app_id = '633953947466193'
my_app_secret = '2d471ec8a8a4f412cf2d3bec9ef6ee64'
my_access_token = 'EAAJAkZBfXudEBABsZCVT1flnVOVDZBsHfoeUje3uIhhca38hxGfajvLi9ESsuJTZAzNMtjWWXJ8JCE2tjK9HGzYyfcU8DVmcAJyE4rZCG2aa3KXt82rxRQdTnehyb7RR15zGcm7OwN9QMHQj31RLPF9oJTDZAeblFnYlXStziapSp5xw2KI4N0'
# FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
# my_account = AdAccount('act_2408768415887341')
url='https://graph.facebook.com/v7.0/23844702031160758/insights?access_token=my_access_token&appsecret_proof=my_app_secret'


camp =requests.get(url)
print(camp)

# curl -G \
# -d "date_preset=last_7d" \
# -d "access_token=<ACCESS_TOKEN>" \
# "https://graph.facebook.com/<API_VERSION>/<AD_CAMPAIGN_ID>/insights"
