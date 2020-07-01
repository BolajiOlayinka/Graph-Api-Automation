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


weekly_data = []
for my_campaigns in campaigns: 
    name  = my_campaigns['campaign_name'].split("@")[0].lower()
    # name  = " ".join(my_campaigns['campaign_name'].split()[:2])
    campaign = {}
    try:
        value = [ i.get("value")  for i in my_campaigns['actions'] if i.get("action_type") == "landing_page_view" ][0]
        campaign['campaign_name'] = my_campaigns['campaign_name'].split("@")[0].lower()
        campaign['calc_cpc'] = int(float(my_campaigns['spend'])) / int(float(value))
        campaign['impressions'] = my_campaigns['impressions']
        campaign['campaign_id'] = my_campaigns['campaign_id']
        campaign['spend'] = my_campaigns['spend']
        campaign['landing_page_view'] = value
        # campaign['action'] = my_campaigns['action']
        weekly_data.append(campaign)
    except Exception as e:
        print(e)
    # print(result)
# print(weekly_data)
# print(weekly_data)
week_data=[]
reading_data=[]
for week in weekly_data:
    # print(week)
    product_name=((week)['campaign_name']) + '.csv'
    print(product_name) 
    with open(product_name, 'a', newline='') as f:
        fields=list(week.keys())
        
        #print(fields)
        output=csv.DictWriter(f, fieldnames=fields) 
        #output.writeheader()
        output.writerow(week)
        #break
    with open(product_name, newline='') as read_csv:
        #user_reader=csv.DictReader(read_csv, delimiter=" ")
        user_reader=csv.DictReader(read_csv)
        user_reader_list=(list(user_reader))
        #print(user_reader_list)
        week_axis = []
        cpc_axis = []
        ctr_axis = []
        count = 0
        for item in user_reader_list:
            cpc_axis.append(item['calc_cpc'])
            result_fb = float(item['landing_page_view'])
            impression_fb = float(item['impressions'])
            count+=1
            #print(result_fb)
            #print(impreesion_fb)
            ctr_axis.append(result_fb/impression_fb)
        folder = os.mkdir(f"figures/week_{len(cpc_axis)}cpc")
        week_axis = range(len(cpc_axis))
        plt.figure()
        plt.scatter(week_axis, cpc_axis)
        plt.savefig(f"figures/week_{len(cpc_axis)}cpc/{count}.png")
        folder = os.mkdir(f"figures/week_{len(cpc_axis)}ctr")
        plt.figure()
        plt.scatter(week_axis, ctr_axis)
        plt.savefig(f"figures/week_{len(cpc_axis)}ctr/{count}.png")
        
        
    break

"""
x=[]
for items in reading_data:
    x.append(items['campaign_name'])
print(x)

# y=[]
# for items in user_reader_list:
# y.append(items['calc_cpc'])
# print(y)
# plt.figure()
# plt.scatter(x,y)
# plt.show()
# for i in range(len(result)):
#     plt.figure()
#     plt.scatter(x[i],y[i])
#     plt.shw()
        # x=(list(user_reader)['campaign_name'])
        # y=(list(user_reader)['calc_cpc'])
        # print(x)
        # plt.figure()
        # plt.scatter(x,y)
        
        #for row in user_reader:
            #print(row)
        



# for week in weekly_data:
#     csv_head=list(week.keys())
#     print(csv_head)
#     product_name=((week)['campaign_name'])
#     with open(product_name, mode='a') as output:
#         output=csv.DictWriter(week, fieldnames=product_name)


      









# for data in weekly_data:
#     product_name = list(data)[0] + '.json'
#     with open(product_name, 'a',  delimeter=',') as file:
#         json.dump(data, file)


"""