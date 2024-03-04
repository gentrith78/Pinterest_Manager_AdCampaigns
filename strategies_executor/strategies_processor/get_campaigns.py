try:
    from .api_call_m import ApiCall
except:
    from api_call_m import ApiCall


class FilterCampaigns():
    def status_filter(self,operator_,status, adacc_id, api_token):
        if operator_ == "IS":
            if status == 'A':
                status = 'ACTIVE'
            if status == 'I':
                status = 'PAUSED'
            return ApiCall(api_token,adacc_id).get_campaignsList(status)
        if operator_ == 'IN':
            if status == 'A':
                status = 'PAUSED'
            if status == 'I':
                status = 'ACTIVE'
            return ApiCall(api_token,adacc_id).get_campaignsList(status)
            pass
    def status_id(self,operator_,campaign_id,adacc_id,api_token):
        campaign_list = ApiCall(api_token, adacc_id).get_campaignsList('ACTIVE')
        if operator_ == 'IS':
            for campaign in campaign_list:
                if int(campaign.id) == campaign_id:
                    return [campaign]
        if operator_ == 'IN':
            campaigns = []
            for campaign in campaign_list:
                if int(campaign.id) == campaign_id:
                    continue
                campaigns.append(campaign)
            return campaigns

        pass
