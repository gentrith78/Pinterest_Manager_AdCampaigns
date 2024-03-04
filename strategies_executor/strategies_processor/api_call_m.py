import datetime
import requests
from dataclasses import dataclass

try:
    from .structured_data import *
except:
    from structured_data import *


class ApiCall():
    """
    - With get_campaignsList(self): get all active campaigns and list them into website
    - With  def get_campaign_analytics(self, campaign_id): get the monitoring data: ROAS, Total Spended,
       Initial Budget (the budget that the advertiser planned to spend on this campaign),
       and the number of sales (TOTAL_CHECKOUT_VALUE_IN_MICRO_DOLLAR)
    """
    def __init__(self, access_token, ad_account_id):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.headers = {'Authorization':f'Bearer {self.access_token}'}

    def get_campaignsList(self,status):
        endpoint = f'https://api.pinterest.com/v5/ad_accounts/{self.ad_account_id}/campaigns'
        params = {
            'entity_statuses':status
        }
        campaigns = requests.get(endpoint, headers=self.headers, params=params).json()
        campaigns_list = []
        for campaign in campaigns['items']:
            try:
                campaign_obj = CampaignItem(id=campaign['id'], name=campaign['name'], status=campaign['status'],
                                lifetime_spend_cap=campaign['lifetime_spend_cap'],daily_spend_cap=campaign['daily_spend_cap'])
                campaigns_list.append(campaign_obj)
            except:
                pass
        return campaigns_list

    def get_dates(self,granularity):
        today = datetime.date.today()

        granularity_to_date_range = {
            'T': [today, datetime.date.today()],
            'TY': [today - datetime.timedelta(days=1), today],
            'Y': [today - datetime.timedelta(days=1), datetime.date.today() - datetime.timedelta(days=1)],
            'LTDT': [today - datetime.timedelta(days=2), datetime.date.today()],
            'LTD': [today - datetime.timedelta(days=3), datetime.date.today() - datetime.timedelta(days=1)],
            'LWD': [today - datetime.timedelta(days=6), today],
            'LW': [today - datetime.timedelta(days=7), today - datetime.timedelta(days=1)],
            'LS': [today - datetime.timedelta(days=6), today],  # not aplied
            'LM': [today - datetime.timedelta(days=29), today],  # not aplied
            'LY': [today.replace(year=today.year - 1), today],  # not aplied
        }

        start_date = granularity_to_date_range[granularity][0].strftime('%Y-%m-%d')
        end_date = granularity_to_date_range[granularity][1].strftime('%Y-%m-%d')
        return start_date, end_date
        pass

    def get_campaign_analytics(self, campaign_id,granularity,variable):
        endpoint = f'https://api.pinterest.com/v5/ad_accounts/{self.ad_account_id}/campaigns/analytics'
        start_date,end_date = self.get_dates(granularity)

        variable_mapper = {
            'TCPCH':'PAGE_VISIT_COST_PER_ACTION',
            'TCOCH':'TOTAL_CHECKOUT_VALUE_IN_MICRO_DOLLAR',
            'ROASC':'CHECKOUT_ROAS',
            'ROASA':'TOTAL_CLICK_ADD_TO_CART',
            'TCAC':'TOTAL_CONVERSIONS',
            'CTR':'CTR',
            'SP':'SPEND_IN_DOLLAR',
            'LSC':'CAMPAIGN_LIFETIME_SPEND_CAP',
            'DSC':'CAMPAIGN_DAILY_SPEND_CAP',
        }

        params = {
            "campaign_ids": [campaign_id],
            "start_date": start_date, # Format: YYYY-MM-DD. Cannot be more than 90 days back from today.
            "end_date": end_date, # Format: YYYY-MM-DD. Cannot be more than 90 days back from today.
            'columns': [variable_mapper[variable]],# SPEND_IN_DOLLAR, TOTAL_CHECKOUT, CHECKOUT_ROAS, CAMPAIGN_LIFETIME_SPEND_CAP, TOTAL_CLICK_CHECKOUT
            "granularity": 'DAY', #can be month, "TOTAL" "DAY" "HOUR" "WEEK" "MONTH"
        }

        campaign_data = requests.get(endpoint, headers=self.headers,params=params).json()
        total_sum = 0
        for data in campaign_data:
            total_sum += data[variable_mapper[variable]]
        return total_sum

    def update_campaign_dsp(self, adacc_id,campaign_id,dsp:int):#dsp = daily spend cap
        endpoint = f"https://api.pinterest.com/v5/ad_accounts/{adacc_id}/campaigns"
        params = {
            "id": str(campaign_id),
            "ad_account_id": adacc_id,
            "daily_spend_cap": dsp,
        }
        campaign_data = requests.patch(endpoint, headers=self.headers,params=params)

