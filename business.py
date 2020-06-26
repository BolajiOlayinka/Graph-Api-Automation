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
for my_campaigns in campaigns:
    my_campaigns.update({'calc_cpc' : int(float(my_campaigns['spend'])) / int(float(my_campaigns['actions'][0]['value'])) } )
    result.append(my_campaigns)
    # print(result)


with open('data.csv', 'a') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(result)

data_read=[]
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for read in csv_reader:
        data_read.append(read)

print(data_read)
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
#     plt.show()






# plt.scatter(x,y)
# plt.show()
# print(y)


# for i in x:
#       for j in y:
#            print(i)
#            print(j)
#            plt.plot(i,j)
#            plt.show()


