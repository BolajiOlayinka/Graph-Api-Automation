import facebook_business
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
import csv 
from matplotlib import pyplot as plt 
import json
import os
import calendar
import time
import numpy as np
plt.rcParams.update({'figure.max_open_warning': 0})

my_app_id = '2725706687661342'
my_app_secret = '259338521f39f49cacef7db0aae1ae5d'
my_access_token = 'EAAmvBArhRR4BADniGjZCgCluOLCRF7TolKU5UriWVmrBH6OUlBypAQgnx0nyPf2wimk3R4bRRQuuLzCbsR82a3DWtYnFMp8ndYTJbdLZBZBHgQQesfC1WjPYeLAYc4T4WoLZBL70olMwpOZBtH7gU7DWclHfDa2xGaMDZAhFOlw4D1SQZCl43F0'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_2408768415887341')

ts = calendar.timegm(time.gmtime())
time = time.ctime(ts)

params = {
    'level': 'campaign',
    'date_preset': 'last_week_sun_sat'
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


with open('shopify_sales.csv', newline='') as read_shopify_csv:
    shopify_reader=csv.DictReader(read_shopify_csv)
    shopify_reader_list=(list(shopify_reader))

with open('product_campaign_name_dictionary.csv') as product_campaign_name_dictionary:
    product_campaign_name_dic=csv.DictReader(product_campaign_name_dictionary)
    product_campaign_name_list=(list(product_campaign_name_dic))

product_campaign_name_table = {}
for product in product_campaign_name_list:
    product_campaign_name_table[product['product_title']] = product['campaign_name']


campaign_list = []
for my_campaigns in campaigns: 
    # name  = my_campaigns['campaign_name'].split("@")[0].lower()
    # name  = " ".join(my_campaigns['campaign_name'].split()[:2])
    campaign = {}
    try:
        value = [ i.get("value")  for i in my_campaigns['actions'] if i.get("action_type") == "landing_page_view" ][0]
        if my_campaigns['campaign_name'].split("@")[0].lower()[-2:] == "ph":
            continue
        elif my_campaigns['campaign_name'].split("@")[0].lower()[-2:] == "ab":
            continue
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
        print(campaign['campaign_name'])
    except Exception as e:
        print(e)


for each_campaign in campaign_list:
    for shopify_item in shopify_reader_list:      
        if (each_campaign)['campaign_name'] == product_campaign_name_table[(shopify_item['product_title'])].lower():
            each_campaign['product_title']=shopify_item['product_title']
            each_campaign['product_vendor']=shopify_item['product_vendor']
            each_campaign['net_quantity']=float(shopify_item['net_quantity'])
            each_campaign['total_sales']=float(shopify_item['total_sales'])      
            each_campaign['total_cost']=float(shopify_item['total_cost']) 
            each_campaign['purchase_rate']=float(each_campaign['net_quantity'])/float(each_campaign['landing_page_view'])
            each_campaign['capital_roi']=((each_campaign['total_sales']-each_campaign['spend']-each_campaign['total_cost'])/(each_campaign['spend']+each_campaign['total_cost'])) * (each_campaign['net_quantity']/each_campaign['spend'])
    if each_campaign.get('net_quantity') == None:
        each_campaign['product_title']=None
        if "focallure" in each_campaign['campaign_name']:
            each_campaign['product_vendor']='focallure'
        elif "sace lady" in each_campaign['campaign_name']:
            each_campaign['product_vendor']='sace lady'
        else:
            each_campaign['product_vendor']=None
        each_campaign['net_quantity']=0
        each_campaign['total_sales']=0      
        each_campaign['total_cost']=0
        each_campaign['purchase_rate']=None
        each_campaign['capital_roi']=None


product_titles_list = []
for each_campaign in campaign_list:
    product_titles_list.append(each_campaign['product_title'])

for shopify_item in shopify_reader_list: 
    if product_titles_list.count(shopify_item['product_title']) >= 1:
        continue
    else:
        new_dictionary = {}
        new_dictionary['campaign_name'] = None
        new_dictionary['date_start'] = None
        new_dictionary['date_stop'] = time
        new_dictionary['impressions'] = 0
        new_dictionary['landing_page_view'] = 0
        new_dictionary['spend'] = 0
        new_dictionary['calc_cpc'] = None
        new_dictionary['calc_ctr'] = None
        new_dictionary['product_title']=shopify_item['product_title']
        new_dictionary['product_vendor']=shopify_item['product_vendor']
        new_dictionary['net_quantity']=float(shopify_item['net_quantity'])
        new_dictionary['total_sales']=float(shopify_item['total_sales'])  
        if shopify_item['total_cost']=='':
            new_dictionary["total_cost"]=0
        else:
            new_dictionary['total_cost']=float(shopify_item['total_cost'])
        campaign_list.append(new_dictionary)


for each_campaign in campaign_list:
    #with open('campaign_list.csv', 'w', newline='') as total_campaign_list:
    with open('campaign_list.csv', 'w') as total_campaign_list:
        campaign_list_header=list(each_campaign.keys())
            #print(fields)
        output=csv.DictWriter(total_campaign_list, fieldnames=campaign_list_header) 
        fileEmpty = os.stat('campaign_list.csv').st_size == 0
        if fileEmpty:
            output.writeheader()
        output.writerow(each_campaign)

#Create chart and file for each single products first below
##################################################
for each_campaign in campaign_list:
    if each_campaign['campaign_name'] == None:
        continue

    product_name=((each_campaign)['campaign_name']) + '.csv'
    print(product_name)
    with open(product_name, 'a', newline='') as product_evaluation_report:
        file_header=list(each_campaign.keys())
        #print(fields)
        output=csv.DictWriter(product_evaluation_report, fieldnames=file_header) 
        fileEmpty = os.stat(product_name).st_size == 0
        if fileEmpty:
            output.writeheader()
        output.writerow(each_campaign)
        #break
    with open(product_name, newline='') as read_csv:
        product_records=csv.DictReader(read_csv)
        product_records_list=(list(product_records))
        cpc_axis=[]
        ctr_axis=[]
        purchase_rate_axis=[]
        capital_roi = []
        stop_date=[]
        date=[]
        count = 0
        for each_product_record in product_records_list:
            cpc_axis.append(float(each_product_record['calc_cpc']))
            stop_date.append(each_product_record['date_stop'])
            ctr_axis.append(float(each_product_record['calc_ctr']))
            print(each_product_record['campaign_name'])
            if each_product_record['purchase_rate'] == '':
                purchase_rate_axis.append(0)
            else:
                purchase_rate_axis.append(float(each_product_record['purchase_rate']))
            if each_product_record['capital_roi'] == '':
                capital_roi.append(0)
            else:
                capital_roi.append(float(each_product_record['capital_roi']))
        # print(item)
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
        plt.savefig(f"{((each_campaign)['campaign_name'])}")

        
##################################################
print("All single products evaluation are completed")
print("All single products evaluation are completed")
print("All single products evaluation are completed")
#Create chart and file for beauty collection below
##################################################

beauty_collection_sales = 0
beauty_collection_spend = 0
beauty_collection_cost = 0
beauty_collection_quantity = 0
collection_name = "beauty.csv"

for each_campaign in campaign_list:
    # print(each_campaign['product_vendor'])
    # print(type(each_campaign['product_vendor']))
    if each_campaign['product_vendor'].lower() == "sace lady":
        print(each_campaign['total_sales'])
        print(type(each_campaign['total_sales']))
        beauty_collection_sales += each_campaign['total_sales']
        beauty_collection_spend += each_campaign['spend']
        beauty_collection_cost += each_campaign['total_cost']
        beauty_collection_quantity += each_campaign['net_quantity']
    
        with open(collection_name, 'a', newline='') as beauty_evaluation_report:
            file_header=list(each_campaign.keys())
            #print(fields)
            output=csv.DictWriter(beauty_evaluation_report, fieldnames=file_header) 
            fileEmpty = os.stat(collection_name).st_size == 0
            if fileEmpty:
                output.writeheader()
            output.writerow(each_campaign)

    elif each_campaign['product_vendor'].lower() == "focallure":
        beauty_collection_sales += each_campaign['total_sales']
        print(type(each_campaign['total_sales']))
        beauty_collection_spend += each_campaign['spend']
        beauty_collection_cost += each_campaign['total_cost']
        beauty_collection_quantity += each_campaign['net_quantity']
        with open(collection_name, 'a', newline='') as beauty_evaluation_report:
            file_header=list(each_campaign.keys())
            #print(fields)
            output=csv.DictWriter(beauty_evaluation_report, fieldnames=file_header) 
            fileEmpty = os.stat(collection_name).st_size == 0
            if fileEmpty:
                output.writeheader()
            output.writerow(each_campaign)
    else:
        continue

beauty_collection_current_week = {}
beauty_collection_current_week['campaign_name'] = "Beauty Collection"
beauty_collection_current_week['data_start'] = None
beauty_collection_current_week['data_stop'] = time
beauty_collection_current_week['impressions'] = None
beauty_collection_current_week['landing_page_views'] = None
beauty_collection_current_week['spend'] = beauty_collection_spend
beauty_collection_current_week['calc_cpc'] = None
beauty_collection_current_week['calc_ctr'] = None
beauty_collection_current_week['product_title'] = "Beauty Collection"
beauty_collection_current_week['product_vendor'] = "Sace Lady & Focallure"
beauty_collection_current_week['net_quantity'] = beauty_collection_quantity
beauty_collection_current_week['total_sales'] = beauty_collection_sales
beauty_collection_current_week['total_cost'] = beauty_collection_cost
beauty_collection_current_week['purchase_rate'] = None
beauty_collection_current_week['capital_roi'] = ((beauty_collection_sales - beauty_collection_spend - beauty_collection_cost)/(beauty_collection_spend + beauty_collection_cost))*(beauty_collection_quantity/beauty_collection_spend)
with open(collection_name, 'a', newline='') as beauty_evaluation_report:
    file_header=list(beauty_collection_current_week.keys())
    output=csv.DictWriter(beauty_evaluation_report, fieldnames=file_header) 
    fileEmpty = os.stat(collection_name).st_size == 0
    if fileEmpty:
        output.writeheader()
    output.writerow(beauty_collection_current_week)