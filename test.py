import facebook_business
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
import csv 
from matplotlib import pyplot as plt 
import json
import os
plt.rcParams.update({'figure.max_open_warning': 0})




my_app_id = '2725706687661342'
my_app_secret = '259338521f39f49cacef7db0aae1ae5d'
my_access_token = 'EAAmvBArhRR4BADniGjZCgCluOLCRF7TolKU5UriWVmrBH6OUlBypAQgnx0nyPf2wimk3R4bRRQuuLzCbsR82a3DWtYnFMp8ndYTJbdLZBZBHgQQesfC1WjPYeLAYc4T4WoLZBL70olMwpOZBtH7gU7DWclHfDa2xGaMDZAhFOlw4D1SQZCl43F0'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_2408768415887341')

params = {
    'level': 'campaign',
    'date_preset': 'this_week_sun_today'
    # 'date_preset': 'this_week_sun_today'
    
}
fields = [
    'campaign_id',
    'campaign_name',
    'impressions',
    'spend',
    'impressions',
    'actions'
]

campaigns = my_account.get_insights(
  fields=fields,
  params=params)
# print(campaigns)

try:
    filer = open("data.json", 'r')
    result = json.load(filer)
except FileNotFoundError:
    result=[]

weekly_data = []
for my_campaigns in campaigns:
    
    name  = my_campaigns['campaign_name'].split("@")[0].lower()
    # name  = " ".join(my_campaigns['campaign_name'].split()[:2])
    
    campaign = {}


    try:
        value = [ i.get("value")  for i in my_campaigns['actions'] if i.get("action_type") == "landing_page_view" ][0]
        campaign['calc_cpc'] = int(float(my_campaigns['spend'])) / int(float(value))
        campaign['impressions'] = my_campaigns['impressions']
        campaign['campaign_id'] = my_campaigns['campaign_id']
        campaign['campaign_name'] = my_campaigns['campaign_name']
        campaign['spend'] = my_campaigns['spend']
        campaign['landing_page_view'] = value
        # campaign['action'] = my_campaigns['action']
        
        weekly_data.append({name:campaign})

    except Exception as e:
        print(e)
    # print(result)
result.append(weekly_data)


# with open('data.json', 'w') as json_file:
#     json.dump(result, json_file)
with open('data.json', 'w') as json_file:
    json_file.write(json.dumps(result, indent=4))

current_products = [list(i.keys())[0] for i in weekly_data]

plot_data = {}
for week in result:
    for item in week:
      
        item_name = list(item.keys())[0]
        
        if item_name in current_products:
            if item_name in plot_data:

                plot_data[item_name].append(item[item_name].get("calc_cpc"))
            else:
                value = [item[item_name].get("calc_cpc")]
                plot_data[item_name] = value




plt.figure(len(current_products))
folder = os.mkdir(f"plots/week_{len(result)}")
for i in current_products:
    plt.figure(current_products.index(i))
    count = 1
    week = []
    for j in plot_data[i]:
        
        week.append(f"{i}_{count}")
        count += 1
        2

    plt.scatter(week,plot_data[i]) 
    plt.savefig(f"plots/week_{len(result)}/{i}_{count}.png")

for data in weekly_data:
    product_name = list(data)[0] + '.json'
    with open(product_name, mode='a') as json_file:
        json_file.write(json.dumps(data, indent=4))

# for data in weekly_data:
#     product_name = list(data)[0] + '.json'
#     with open(product_name, 'a',  delimeter=',') as file:
#         json.dump(data, file)

