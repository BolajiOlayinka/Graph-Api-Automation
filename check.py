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
    
weekly_data = []
for my_campaigns in campaigns: 
    name  = my_campaigns['campaign_name'].split("@")[0].lower()
    # name  = " ".join(my_campaigns['campaign_name'].split()[:2])
    campaign = {}
    try:
        value = [ i.get("value")  for i in my_campaigns['actions'] if i.get("action_type") == "landing_page_view" ][0]
        campaign['calc_cpc'] = round(int(float(my_campaigns['spend'])) / int(float(value)),2)
        campaign['impressions'] = my_campaigns['impressions']
        campaign['campaign_id'] = my_campaigns['campaign_id']
        campaign['campaign_name'] = my_campaigns['campaign_name'].split("@")[0].lower()
        campaign['spend'] = my_campaigns['spend']
        campaign['landing_page_view'] = value
        campaign['current_time'] = time
        campaign['calc_ctr'] = round(int(float(value))/int(float(my_campaigns['impressions'])),4)
        weekly_data.append(campaign)
    except Exception as e:
        print(e)

for week in weekly_data:
    product_name=((week)['campaign_name']) + '.csv'
    for shopify_item in shopify_reader_list:
        if (week)['campaign_name'] == (shopify_item['product_title']).lower():
            week['net_quantity']=shopify_item['net_quantity']
            week['total_sales']=shopify_item['total_sales']       
        print(week)
        with open(product_name, 'a', newline='') as f:
            fields=list(week.keys())
            #print(fields)
            output=csv.DictWriter(f, fieldnames=fields) 
            fileEmpty = os.stat(product_name).st_size == 0
            if fileEmpty:
                output.writeheader()
            output.writerow(week)
            #break
        with open(product_name, newline='') as read_csv:
            user_reader=csv.DictReader(read_csv)
            user_reader_list=(list(user_reader))
            # week_axis=[]
            cpc_axis=[]
            ctr_axis=[]
            purchase_rate_axis=[]
            capital_roi = []
            count = 0
            for item in user_reader_list:
                cpc_axis.append(item['calc_cpc'])
                result_fb = float(item['landing_page_view'])
                impression_fb = float(item['impressions'])
                orders_shopify = float(item['net_quantity'])
                # week_axis.append(item['current_time'])
                count+=1
                #print(result_fb)
                #print(impreesion_fb)
                ctr_axis.append(result_fb/impression_fb)
                purchase_rate_axis.append(orders_shopify/result_fb)
                capital_roi.append(count)
            plt.figure()
            plt.subplot(221)
            plt.plot(cpc_axis)
            plt.title('Cpc')
            plt.grid(True)    
            plt.subplot(222)
            plt.plot(ctr_axis)
            plt.title('Ctr')
            plt.grid(True)
            plt.subplot(223)
            plt.plot(purchase_rate_axis)
            plt.title('Purchase Rate')
            plt.grid(True)
            plt.subplot(224)
            plt.plot(capital_roi)
            plt.title('Capital Roi')
            plt.grid(True)
            plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,wspace=0.35)
            plt.show()
        break
    break

