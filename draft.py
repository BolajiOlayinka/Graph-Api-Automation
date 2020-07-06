import facebook_business
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
import csv 
from matplotlib import pyplot as plt 
import json
import os
plt.rcParams.update({'figure.max_open_warning': 0})
import calendar
import time
import numpy as np

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
    'date_start',
    'date_stop',
    'actions'
]

campaigns = my_account.get_insights(
  fields=fields,
  params=params)
# print(campaigns)

ts = calendar.timegm(time.gmtime())
time = time.ctime(ts)


with open('shopify_sales.csv', newline='') as read_shopify_csv:
    shopify_reader=csv.DictReader(read_shopify_csv)
    shopify_reader_list=(list(shopify_reader))
    
campaign_list = []
for my_campaigns in campaigns: 
    # name  = my_campaigns['campaign_name'].split("@")[0].lower()
    # name  = " ".join(my_campaigns['campaign_name'].split()[:2])
    campaign = {}
    try:
        value = [ i.get("value")  for i in my_campaigns['actions'] if i.get("action_type") == "landing_page_view" ][0]
        campaign['campaign_name'] = my_campaigns['campaign_name'].split("@")[0].lower()
        campaign['date_start'] = my_campaigns['date_start']
        campaign['date_stop'] = time
        campaign['impressions'] = float(my_campaigns['impressions'])
        campaign['landing_page_view'] = value
        campaign['spend'] = float(my_campaigns['spend'])
        campaign['calc_cpc'] = round(int(float(my_campaigns['spend'])) / int(float(value)),2)
        #campaign['current_time'] = time
        campaign['calc_ctr'] = round(int(float(value))/int(float(my_campaigns['impressions'])),4)
        campaign_list.append(campaign)
    except Exception as e:
        print(e)
for each_campaign in campaign_list:
    file_name=((each_campaign)['campaign_name'])
    product_name=((each_campaign)['campaign_name']) + '.csv'
    for shopify_item in shopify_reader_list:
        if (each_campaign)['campaign_name'] == (shopify_item['campaign_name']).lower():
            each_campaign['net_quantity']=float(shopify_item['net_quantity'])
            each_campaign['total_sales']=float(shopify_item['total_sales'])      
            each_campaign['cost']=float(shopify_item['cost']) 
            each_campaign['capital_roi']=((each_campaign['total_sales']-each_campaign['spend']-each_campaign['cost'])/(each_campaign['spend']+each_campaign['cost'])) * (each_campaign['net_quantity']/each_campaign['spend'])
    if each_campaign.get('net_quantity') == None:
        continue

    print((each_campaign)['campaign_name'])
    with open(product_name, 'a', newline='') as f:
        fields=list(each_campaign.keys())
        #print(fields)
        output=csv.DictWriter(f, fieldnames=fields) 
        fileEmpty = os.stat(product_name).st_size == 0
        if fileEmpty:
            output.writeheader()
        output.writerow(each_campaign)
        #break
    with open(product_name, newline='') as read_csv:
        user_reader=csv.DictReader(read_csv)
        user_reader_list=(list(user_reader))
        # each_campaign_axis=[]
        cpc_axis=[]
        ctr_axis=[]
        purchase_rate_axis=[]
        capital_roi = []
        stop_date=[]
        date=[]
        count = 0
        for item in user_reader_list:
            cpc_axis.append(float(item['calc_cpc']))
            result_fb = float(item['landing_page_view'])
            impression_fb = float(item['impressions'])
            orders_shopify = float(item['net_quantity'])
            stop_date.append(item['date_stop'])
            ctr_axis.append(float(item['calc_ctr']))
            purchase_rate_axis.append(orders_shopify/result_fb)
            capital_roi.append(float(item['capital_roi']))
        print(item)
        plt.rc('xtick', labelsize=6)
        plt.rc('ytick', labelsize=6)
        plt.figure()
        plt.subplot(221)
        plt.xticks(rotation=45, ha="right")
        plt.plot(stop_date,cpc_axis,'-o')
        plt.title('Cpc')
        plt.grid(True)    
        plt.subplot(222)
        plt.xticks(rotation=45, ha="right")
        plt.plot(stop_date,ctr_axis,'-o')
        plt.title('Ctr')
        plt.grid(True)
        plt.subplot(223)
        plt.xticks(rotation=45, ha="right")
        plt.plot(stop_date,purchase_rate_axis,'-o')
        plt.title('Purchase Rate')
        plt.grid(True)
        plt.subplot(224)
        plt.xticks(rotation=45, ha="right")
        plt.plot(stop_date,capital_roi,'-o')
        plt.title('Capital Roi')
        plt.grid(True)
        plt.subplots_adjust(top=0.92, bottom=0.2, left=0.15, right=0.95, hspace=1.0,wspace=0.5)
        plt.savefig(f"{file_name}")
            


