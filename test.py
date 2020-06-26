import facebook_business
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
import csv 
from matplotlib import pyplot as plt 
import json
import os




my_app_id = '633953947466193'
my_app_secret = '2d471ec8a8a4f412cf2d3bec9ef6ee64'
my_access_token = 'EAAJAkZBfXudEBABsZCVT1flnVOVDZBsHfoeUje3uIhhca38hxGfajvLi9ESsuJTZAzNMtjWWXJ8JCE2tjK9HGzYyfcU8DVmcAJyE4rZCG2aa3KXt82rxRQdTnehyb7RR15zGcm7OwN9QMHQj31RLPF9oJTDZAeblFnYlXStziapSp5xw2KI4N0'
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
    
    # name  = my_campaigns['campaign_name'].split("_")[0].lower()
    name  = " ".join(my_campaigns['campaign_name'].split()[:2])
    
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


with open('data.json', 'w') as json_file:
    json.dump(result, json_file)

# data_read=[]
# with open('data.csv') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     for read in csv_reader:
#         data_read.append(read)


# print(len(data_read[2]))
# print(data_read[0])
# for data in data_read:
#     print(data[1])

# data_list = [] 
# for l in data_read:
#     temp_data = l[0]
#     data_list.append(temp_data)

# print (data_list)
# print(age_list)
# with open("data.txt", "w") as txt_file:
#     for line in result:
#         txt_file.write(line)


    
# with open('data.txt', 'w') as outfile:
#     json.dump(result, outfile )


# with open("data.txt","w") as outfile:
#     outfile.write(result)


# print(result[0])

# x=[]
# for items in result:
#       x.append(items['campaign_name'])

# y=[]
# for items in result:
#       y.append(items['calc_cpc'])

# for i in range(len(result)):
#     plt.figure()
#     plt.scatter(x[i],y[i])
#     plt.shw()

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
        
        # plt.scatter(f"{i}_{count}",j)
        week.append(f"{i}_{count}")
        count += 1
        

    plt.scatter(week,plot_data[i]) 
    plt.savefig(f"plots/week_{len(result)}/{i}_{count}.png")








# plt.scatter(x,y)
# plt.show()
# print(y)


# for i in x:
#       for j in y:
#            print(i)
#            print(j)
#            plt.plot(i,j)
#            plt.show()


