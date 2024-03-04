from django.db import models

#there should be added a user model that will be able to create an add account

class AdAccount(models.Model):
    name = models.CharField(max_length=255,default='')
    api_token = models.CharField(max_length=255,default='')
    ad_account_id = models.CharField(max_length=255,default='')


class Rule_Item(models.Model):
    STATUS_TYPES = [
            ('A', "Active"),
            ('I', 'Inactive'),
        ]
    ad_acc = models.ForeignKey(AdAccount, models.CASCADE,related_name='strategy')# TODO integrate new realtions
    name = models.CharField(max_length=255,default='')
    description = models.TextField(max_length=255,default='')
    status = models.CharField(max_length=1,choices=STATUS_TYPES,default='A')

class Filter(models.Model):
    OPERATOR = [
        ("D",'Choose Operator'),
        ('A',"All"),
        ('O','At Least One')
    ]
    FILTER_TYPE = [
        ('D', 'Initial'),
        ('S',"By Status"),
        ('I','By Id')
    ]
    rule_item = models.ForeignKey(Rule_Item, on_delete=models.CASCADE, related_name='filter')
    filter_type = models.CharField(max_length=1,choices=FILTER_TYPE,default='D')
    operator_choice = models.CharField(max_length=1, choices=OPERATOR, default='A')


class FilterStatus(models.Model):
    STATUS_TYPES = [
            ('D', "Select Status"),
            ('A', "Active"),
            ('I', 'Inactive'),
        ]

    CONDITION_TYPES = [
        ('IS','Is'),
        ('IN','Is Not'),
    ]
    filter = models.ForeignKey(Filter,null=True,on_delete=models.CASCADE)
    condition_choice = models.CharField(max_length=2,choices=CONDITION_TYPES,default='IS')
    status = models.CharField(max_length=1,choices=STATUS_TYPES,default='D')
    confirmed = models.BooleanField(default=False)


class FilterId(models.Model):
    CONDITION_TYPES = [
        ('IS','Is'),
        ('IN','Is Not'),
    ]
    filter = models.ForeignKey(Filter,null=True,on_delete=models.CASCADE)
    condition_choice = models.CharField(max_length=2,choices=CONDITION_TYPES,default='IS')
    #equeal
    value = models.IntegerField(default=0)
    confirmed = models.BooleanField(default=False)


class Condition(models.Model):
    OPERATOR = [
        ("D",'Choose Operator'),
        ('A',"All"),
        ('O','At Least One')
    ]

    rule_item = models.ForeignKey(Rule_Item, on_delete=models.CASCADE, related_name='conditions')
    operator_choice = models.CharField(max_length=1, choices=OPERATOR, default='A')

class ConditionItem(models.Model):
    VARIABLES = [
        ('DEF', 'Select Variable'),
        ('TCPCH', 'Total CPA Checkout'),
        ('TCOCH', 'Total Conversions Checkout'),
        ('ROASC', 'ROAS Checkout'),
        ('ROASA', 'Total ROAS Add to cart'),
        ('TCAC', 'Total Conversions Add to cart'),
        ('CTR', 'CTR'),
        ('SP', 'Spendings'),
        ('LSC','Lifetime Spend Cap'),
        ('DSC','Daily Spend Cap'),
    ]

    GRANULARITY = [
        ('DEF', 'Select Granularity'),
        ('T','Today'),
        ('TY','Today and Yesterday'),
        ('Y','Yesterday'),
        ('LTDT', 'Last Three Days INC. Today'),
        ('LTD','Last Three Days'),
        ('LWD', 'Last Week Inc. Today'),
        ('LW', 'Last Week'),
    ]
    CONDITION = [
        ('DEF', 'Select Condition'),
        ('E', 'Equal'),
        ('NE', 'Not Equal'),
        ('GT','Greater Than'),
        ('GTE', 'Greater Than or Equal'),
        ('LT','Less Than'),
        ('LTE', 'Less Than or Equal'),
    ]
    condition = models.ForeignKey(Condition,on_delete=models.CASCADE)
    variable = models.CharField(max_length=255, choices=VARIABLES, default='DEF')
    granularity = models.CharField(max_length=255, choices=GRANULARITY, default='DEF')
    condition_op = models.CharField(max_length=255, choices= CONDITION, default='DEF')#condition operator
    value = models.CharField(max_length=255,default=0)
    confirmed = models.BooleanField(default=False)

class Action(models.Model):
    ACTIONS = [
        ('IN','Increase Budget'),
        ('SB','Set Budget'),
        ('De','Decrease Budget'),
    ]


    rule_item = models.ForeignKey(Rule_Item,on_delete=models.CASCADE,related_name='action')
    action = models.CharField(max_length=2, choices=ACTIONS, default='IN')
    value = models.CharField(max_length=10,default=0)
    confirmed = models.BooleanField(default=False)

class Interval(models.Model):
    GRANULARITY = [
        ('DEF', 'Select Interval'),
        ('E10', 'Every 10 Min'),
        ('E30','Every 30 Min'),
        ('EH','Every Hour'),
        ('ETH','Every Two Hours'),
        ('ED','Every Day'),
        ('EW','Every Week'),
    ]
    #TODO add EW to the crontab schedules
    rule_item = models.ForeignKey(Rule_Item, on_delete=models.CASCADE)
    interval = models.CharField(max_length=3,choices=GRANULARITY, default='ED')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
