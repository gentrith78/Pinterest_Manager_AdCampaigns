from django import forms
from .models import AdAccount, Rule_Item ,Filter,FilterStatus, FilterId , Condition, ConditionItem, Action, Interval
from crispy_forms.layout import Field

class AdAccount_Form(forms.ModelForm):
    class Meta:
        model = AdAccount
        fields = ['name', 'api_token','ad_account_id']
        labels = {
            'name': 'Ad Account name',
            'api_token': 'Ad Account Token',
            'ad_account_id': 'Ad Account ID',
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": 'col',"placeholder":'Ad Account Name','id':'strategy_name'}),
            "api_token": forms.TextInput(attrs={"class": 'col', "placeholder":' Api Token','id': "strategy_name"}),
            "ad_account_id": forms.TextInput(attrs={"class": 'col', "placeholder":' Add Account Id','id': "strategy_name"})
        }

class Rule_Item_Form(forms.ModelForm):
    class Meta:
        model = Rule_Item
        fields = ['name', 'description']
        labels = {
            'name': '',
            'description': '',
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": 'col-md-6 offset-md-3 ', "placeholder":'Enter Name','id':'strategy_name'}),
            "description": forms.Textarea(attrs={"class": 'col-md-6 offset-md-3', "placeholder":'Enter Description', 'id': "strategy_name"})
        }


class FilterForm(forms.ModelForm):
    class Meta:
        model = Filter
        fields = ['filter_type']
        labels = {
            'operator_choice': '',
            'filter_type': '',

        }
        widgets = {
            "operator_choice": forms.Select(attrs={"class":'col select-filter'}),
            "filter_type": forms.Select(attrs={"class":'col select-filter align-self-center','name':"type"})
        }

class FilterStatusForm(forms.ModelForm):
    class Meta:
        model = FilterStatus
        fields = ['condition_choice','status']
        labels = {
            'condition_choice': '',
            'status': '',
        }
        widgets = {
            "condition_choice": forms.Select(attrs={"class":'col select-filter mx-1'}),
            "status": forms.Select(attrs={"class": 'col select-filter mx-1'}),
        }

class FilterIdForm(forms.ModelForm):
    class Meta:
        model = FilterId
        fields = ['condition_choice','value']
        labels = {
            'condition_choice': '',
            'value': '',
        }
        widgets = {
            "value": forms.NumberInput(attrs={"class":'select-filter'}),
            "condition_choice": forms.Select(attrs={"class":'select-filter'}),
        }


class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields =  ['operator_choice']
        labels = {
            'operator_choice': 'Should Match:'}
        widgets = {
            "operator_choice": forms.Select(attrs={"class":'select-filter'})
        }

class ConditionItemForm(forms.ModelForm):
    class Meta:
        model = ConditionItem
        fields = ('variable','granularity','condition_op','value')
        labels = {
            'variable': '',
            'granularity': '',
            'condition_op': '',
            'value': ''
        }
        widgets = {
            "variable": forms.Select(attrs={"class":'col-2 px-1 ms-0 mt-3 select-filter'}),
            "granularity": forms.Select(attrs={"class":'col-2 px-1 mx-2 mt-3 select-filter'}),
            "condition_op": forms.Select(attrs={"class":'col-3 px-1 mx-2 mt-3 select-filter'}),
            "value": forms.TextInput(attrs={"class":'col-1 px-1 mx-2 mt-3 select-filter','placeholder':'enter value','type':'number','step':'0.01','min':'0.00'}),
        }
class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['action','value']
        labels = {
            'action': '',
            'value': '',
        }
        widgets = {
            "action": forms.Select(attrs={"class":'col px-1 ms-0 mt-3 select-filter'}),
            "value": forms.TextInput(attrs={"class":'col-2 px-1 mx-1','placeholder':'Value','type':'number','step':'0.01','min':'0.00'}),
        }

class IntervalForm(forms.ModelForm):
    class Meta:
        model = Interval
        fields = ['interval']
        labels = {
            'interval': '',
        }
        widgets = {
            "interval": forms.Select(attrs={"class":'col select-filter'}),
        }
