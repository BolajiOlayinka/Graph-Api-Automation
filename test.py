import facebook_business
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
import csv 
from matplotlib import pyplot as plt 
import json



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

result=[]
weekly_data = []
for my_campaigns in campaigns:
    campaign = {}

    try:
        campaign['calc_cpc'] = int(float(my_campaigns['spend'])) / int(float(my_campaigns['actions'][0]['value']))
        campaign['impressions'] = my_campaigns['impressions']
        campaign['impressions'] = my_campaigns['impressions']
        campaign['impressions'] = my_campaigns['impressions']
        campaign['impressions'] = my_campaigns['impressions']
        campaign['impressions'] = my_campaigns['impressions']
        
        my_campaigns.update( )
        result.append(my_campaigns)
    except Exception as e:
        print(e)
    # print(result)


with open('data.json', 'a') as json_file:
    json.dump(json_file, result)

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

x=[]
for items in result:
      x.append(items['campaign_name'])

y=[]
for items in result:
      y.append(items['calc_cpc'])

# for i in range(len(result)):
#     plt.figure()
#     plt.scatter(x[i],y[i])
#     plt.shw()






# plt.scatter(x,y)
# plt.show()
# print(y)


# for i in x:
#       for j in y:
#            print(i)
#            print(j)
#            plt.plot(i,j)
#            plt.show()


