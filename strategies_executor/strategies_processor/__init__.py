import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pinterest_bot.settings')
django.setup()

from rules_app.models import *

try:
    from .api_call_m import ApiCall
    from .get_campaigns import FilterCampaigns
    from .structured_data import *
except:
    from api_call_m import ApiCall
    from get_campaigns import FilterCampaigns
    from structured_data import *


class Strategies():  # this class will return all rule_item objects by giving "interval_type" as input
    def __init__(self, interval_type):
        self.interval_type = interval_type
        self.strategies = self.process()
        pass

    def process(self):
        return Rule_Item.objects.filter(interval__interval=self.interval_type).filter(status='A')
        pass

#lesthan:lt, greater than:gt, equeal:e ...etc

class Strategy(): #here each strategy should be processed and the budget will be modified here
    def __init__(self,rule_item_obj):
        self.strategy_obj = rule_item_obj
        self.token = self.strategy_obj.ad_acc.api_token
        self.ad_account_id = self.strategy_obj.ad_acc.ad_account_id
        self.filter_obj = Filter.objects.get(rule_item=self.strategy_obj)
        self.interval_obj = Interval.objects.get(rule_item=self.strategy_obj)
        self.condition_obj = Condition.objects.get(rule_item=self.strategy_obj)
        self.condition_items = ConditionItem.objects.filter(condition=self.condition_obj).exclude(variable='DEF').exclude(granularity='DEF').exclude(condition_op='DEF') .exclude(value='DEF')
        self.action_obj = Action.objects.get(rule_item=self.strategy_obj)
        self.process()

    def process(self):
        if self.check() == False:
            return False
        #get Campaigns
        campaigns = self.get_campaigns() #list of CampaignItem
        for campaign in campaigns:
            # get comparison objects
            comparison_objects = []
            for condition in self.condition_items:
                received_variable_value = ApiCall(self.token,self.ad_account_id).get_campaign_analytics(campaign.id,condition.granularity,condition.variable)
                if received_variable_value != None:
                    comparison_obj = Comparison(ConditionItem_variable=condition.variable,
                                                ConditionItem_inputted_value=float(condition.value)
                                                , Received_Value=received_variable_value, operator=condition.condition_op
                                                )
                    comparison_objects.append(comparison_obj)

            # compare all comparison objects
            matches = 0
            for comparison in  comparison_objects:
                if self.compare(comparison):
                    matches+=1
                    comparison.match = True
                else:
                    f"NOT MATCH"
            for comp in comparison_objects:
                print(comp)
            #take action
            if self.condition_obj.operator_choice == "A": #all conditions should match
                if matches == len(self.condition_items):
                    self.update_budget(campaign)
            if self.condition_obj.operator_choice == "O": #at least one condition should be match
                if matches>0:
                    self.update_budget(campaign)

    def update_budget(self,campaign_obj):
        if self.action_obj.action == 'IN':
            current_budget = campaign_obj.daily_spend_cap
            budget_to_increment = int(float(self.action_obj.value) * 1000000)
            total_budget = current_budget+budget_to_increment
            # TODO take update budget
            # ApiCall(self.token,self.ad_account_id).update_campaign_dsp(self.ad_account_id,campaign_obj.id,total_budget)
            print(f"for campaign:{campaign_obj.id}--- BUDGET INCREASED --- current: {current_budget} -- to increment:{budget_to_increment} -- total: {total_budget}")
        if self.action_obj.action == 'De':
            current_budget = campaign_obj.daily_spend_cap
            budget_to_decrement = int(float(self.action_obj.value) * 1000000)
            total_budget = current_budget - budget_to_decrement
            # TODO take update budget
            # ApiCall(self.token,self.ad_account_id).update_campaign_dsp(self.ad_account_id,campaign_obj.id,total_budget)
            print(f"for campaign:{campaign_obj.id}--- BUDGET DECREASED --- current: {current_budget} -- to increment:{budget_to_decrement} -- total: {total_budget}")
            pass
        if self.action_obj.action == 'SB':
            total_budget = int(float(self.action_obj.value) * 1000000) #set budget
            # TODO take update budget
            print(f"for campaign:{campaign_obj.id}--- SET BUDGET --- current:-- total: {total_budget}")
            # ApiCall(self.token,self.ad_account_id).update_campaign_dsp(self.ad_account_id,campaign_obj.id,total_budget)

    def get_campaigns(self):
        #get filter type
        if self.filter_obj.filter_type == 'S':
            filter_status = FilterStatus.objects.get(filter=self.filter_obj)
            operator_ = filter_status.condition_choice
            campaign_status = filter_status.status
            return FilterCampaigns().status_filter(operator_,campaign_status,self.ad_account_id,self.token) #list of CampaignItem
        if self.filter_obj.filter_type == 'I':
            filter_id = FilterId.objects.get(filter=self.filter_obj)
            operator_ = filter_id.condition_choice
            campaign_id = filter_id.value
            return FilterCampaigns().status_id(operator_,campaign_id,self.ad_account_id,self.token)
            pass
        pass

    def compare(self,comparison_obj):
        if comparison_obj.operator == 'E':
            return comparison_obj.ConditionItem_inputted_value == comparison_obj.Received_Value
        if comparison_obj.operator == 'NE':
            return comparison_obj.ConditionItem_inputted_value != comparison_obj.Received_Value
        if comparison_obj.operator == 'GT':
            return comparison_obj.ConditionItem_inputted_value < comparison_obj.Received_Value
        if comparison_obj.operator == 'GTE':
            return comparison_obj.ConditionItem_inputted_value <= comparison_obj.Received_Value
        if comparison_obj.operator == 'LT':
            return comparison_obj.ConditionItem_inputted_value > comparison_obj.Received_Value
        if comparison_obj.operator == 'LTE':
            return comparison_obj.ConditionItem_inputted_value >= comparison_obj.Received_Value

    def check(self):#validate strategy
        #check filter
        if self.filter_obj.filter_type == 'D':
            #user hasn't selected the filter type
            return False
        if self.filter_obj.filter_type == 'S':
            filter_status = FilterStatus.objects.get(filter=self.filter_obj)
            if filter_status.confirmed == False:
                #user has not confirmed the filtering type
                return False
        if self.filter_obj.filter_type == 'I':
            filter_id = FilterId.objects.get(filter=self.filter_obj)
            if filter_id.confirmed == False:
                # user has not confirmed the filtering type
                return False
            pass

        #check if there is at least one condition confirmed and that there is not an default value left on that condition
        #in this case in self.condition_items we exclude all condition_item that has at least one default value left so we check only if the length of list is more than 0
        if len(self.condition_items) == 0:
            return False

        #check actions
        if self.action_obj.confirmed == False:
            return False

        #everything is good to go if it reaches here
        return True


def process_strategies(interval):
    import os
    import django

    # Set up the Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pinterest_bot.settings')
    django.setup()

    rule_item_objects = Strategies(interval).strategies
    for rule_item_obj in rule_item_objects:
        strategy_processor = Strategy(rule_item_obj) #process each strategy

if __name__ == '__main__':
    process_strategies('EW')



# SPEND_IN_DOLLAR, TOTAL_CHECKOUT, CHECKOUT_ROAS, CAMPAIGN_LIFETIME_SPEND_CAP, TOTAL_CLICK_CHECKOUT
"""
SPEND_IN_DOLLAR = Total dollar spended for that campaign for data (day)

CAMPAIGN_LIFETIME_SPEND_CAP = Total dollars planned bu the advertiser to spend for the ad campaign

TOTAL_CHECKOUT
TOTAL_CLICK_CHECKOUT


CHECKOUT_ROAS
"""