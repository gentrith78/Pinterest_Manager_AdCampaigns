from django.shortcuts import render, redirect
from .forms import AdAccount_Form,Rule_Item_Form, FilterForm, FilterStatusForm, FilterIdForm, ConditionForm, ConditionItemForm, ActionForm,  IntervalForm
from .models import AdAccount, Rule_Item, Filter, FilterStatus, FilterId,Condition, ConditionItem, Action, Interval
# Create your views here.


def main_page(request):
    strategies = Rule_Item.objects.all()
    context = {
        "strategies":strategies,
    }
    return render(request, 'rules_app/main_page.html',context)

def add_adaccount(request):
    if request.method == 'POST':
        form = AdAccount_Form(request.POST)
        if form.is_valid():
            form.save()
    strategy_form = AdAccount_Form
    context = {
        'strategy_form':strategy_form
    }
    return render(request, 'rules_app/main_page.html')
    pass

def manage_add_account(request,pk):
    ad_acc_obj = AdAccount.objects.get(pk=pk)
    if request.method == 'POST':
        form = AdAccount_Form(request.POST,instance=ad_acc_obj)
        if form.is_valid():
            form.save()

        pass



def dashboard(request): #will contain all  rules of an ad account
    ad_acc = list(AdAccount.objects.all())
    if len(ad_acc)>0:
        ad_acc = ad_acc[0]
        rule_item_obj = Rule_Item.objects.filter(ad_acc=ad_acc)
        ad_acc_form = AdAccount_Form(instance=ad_acc)
    else:
        ad_acc = AdAccount.objects.create()
        rule_item_obj = Rule_Item.objects.filter(ad_acc=ad_acc)
        ad_acc_form = AdAccount_Form(instance=ad_acc)
    if request.method == 'POST':
        form = AdAccount_Form(request.POST,instance=ad_acc)
        if form.is_valid():
            form.save()
            ad_acc = list(AdAccount.objects.all())
            ad_acc = ad_acc[0]
            rule_item_obj = Rule_Item.objects.filter(ad_acc=ad_acc)
            ad_acc_form = AdAccount_Form(instance=ad_acc)

    context = {
        "strategies":rule_item_obj,
        "ad_acc_form":ad_acc_form,
        "ad_acc_obj":ad_acc
    }
    return render(request, 'rules_app/dashboard.html',context)
    pass

def add_filter(request,pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    filter_obj = Filter.objects.get(rule_item=rule_item_obj)
    if request.method == 'POST':
        #find what filter to add
        filter_type = request.POST['filter_type']
        if filter_type == 'S':
            FilterStatus.objects.create(filter=filter_obj)
        if filter_type == 'I':
            FilterId.objects.create(filter=filter_obj)
        form = FilterForm(request.POST, instance=filter_obj)
        if form.is_valid():
            form.save()
    return redirect('rule',pk=rule_item_obj.pk)



def confirm_filter_status(request,pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    filter_obj = Filter.objects.get(rule_item=rule_item_obj)
    filter_status_obj = FilterStatus.objects.get(filter=filter_obj)
    if request.method == 'POST':
        form = FilterStatusForm(request.POST,instance=filter_status_obj)
        if form.is_valid():
            if filter_status_obj.status == 'D':
                pass
            else:
                filter_status_obj.confirmed = True
                filter_status_obj.save()
                form.save()
    return redirect('rule',pk=rule_item_obj.pk)

def delete_filter_status(request, pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    filter_obj = Filter.objects.get(rule_item=rule_item_obj)
    filter_status_obj = FilterStatus.objects.get(filter=filter_obj)
    filter_status_obj.delete()
    filter_obj.filter_type = 'D'
    filter_obj.save()
    return redirect('rule',pk=rule_item_obj.pk)


def confirm_filter_id(request,pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    filter_obj = Filter.objects.get(rule_item=rule_item_obj)
    filter_id_obj = FilterId.objects.get(filter=filter_obj)
    if request.method == 'POST':
        form = FilterIdForm(request.POST,instance=filter_id_obj)
        if form.is_valid():
            filter_id_obj.confirmed = True
            filter_id_obj.save()
            form.save()
    return redirect('rule',pk=rule_item_obj.pk)

def delete_filter_id(request, pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    filter_obj = Filter.objects.get(rule_item=rule_item_obj)
    filter_status_obj = FilterId.objects.get(filter=filter_obj)
    filter_status_obj.delete()
    filter_obj.filter_type = 'D'
    filter_obj.save()
    return redirect('rule',pk=rule_item_obj.pk)

def add_conditionItem(request, pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    condition_obj = Condition.objects.get(rule_item = rule_item_obj)
    condition_item_obj = ConditionItem.objects.create(condition = condition_obj)
    return redirect('rule',pk=rule_item_obj.pk)




def confirm_conditionItem(request, pk, id):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    condition_obj = Condition.objects.get(rule_item = rule_item_obj)
    condition_item_obj = ConditionItem.objects.filter(condition = condition_obj).filter(id=id)[0]
    if request.method == 'POST':
        form = ConditionItemForm(request.POST, instance=condition_item_obj)
        if form.is_valid():
            condition_item_obj.confirmed = True
            condition_item_obj.save()
            form.save()
    return redirect('rule',pk=rule_item_obj.pk)

def update_match_operator(request,pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    condition_obj = Condition.objects.get(rule_item = rule_item_obj)
    if request.method == 'POST':
        if request.POST.get('option_all') == 'all':
            condition_obj.operator_choice = 'A'
            condition_obj.save()

        if request.POST.get('option_all') == 'at least one':
            condition_obj.operator_choice = 'O'
            condition_obj.save()
    return redirect('rule',pk=rule_item_obj.pk)


def delete_conditionItem(request, pk, id):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    condition_obj = Condition.objects.get(rule_item = rule_item_obj)
    condition_item_obj = ConditionItem.objects.filter(condition = condition_obj).filter(id=id)
    condition_item_obj.delete()
    return redirect('rule',pk=rule_item_obj.pk)

def action_confirm(request, pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    action_obj = Action.objects.get(rule_item=rule_item_obj)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=action_obj)
        if form.is_valid():
            action_obj.confirmed = True
            action_obj.save()
            form.save()
    return redirect('rule',pk=rule_item_obj.pk)

def action_delete(request, pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    action_obj = Action.objects.get(rule_item=rule_item_obj)
    action_obj.delete()
    #create new default action
    a = Action.objects.create(rule_item=rule_item_obj)
    return redirect('rule',pk=rule_item_obj.pk)

def add_strategy(request,pk):
    ad_account = AdAccount.objects.get(pk=pk)
    if request.method == "POST":
        rule_item_obj = Rule_Item.objects.create(ad_acc=ad_account)
        form = Rule_Item_Form(request.POST,instance=rule_item_obj)
        form.ad_acc = ad_account
        if form.is_valid():
            #assign this rule to the ad account
            rule_item_obj = form.save()
            # creting other instances
            filter_obj = Filter.objects.create(rule_item=rule_item_obj)
            condition_obj = Condition.objects.create(rule_item=rule_item_obj)
            condition_item_obj = ConditionItem.objects.create(condition=condition_obj)
            action_obj = Action.objects.create(rule_item=rule_item_obj )
            interval_obj = Interval.objects.create(rule_item=rule_item_obj)
            return redirect('rule',pk=rule_item_obj.pk)
    context = {
        'strategy_form':Rule_Item_Form
    }
    return render(request,'rules_app/add_strategy.html',context)

def pause_activate_strategy(request,pk,st):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    if st == "P":
        rule_item_obj.status = 'I'
        rule_item_obj.save()
        return redirect('strategies_page')
    if st == 'A':
        rule_item_obj.status = 'A'
        rule_item_obj.save()
        return redirect('strategies_page')

def confirm_interval(request,pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    interval_obj = Interval.objects.get(rule_item=rule_item_obj)
    if request.method == 'POST':
        form = IntervalForm(request.POST,instance=interval_obj)
        if form.is_valid():
            form.save()
            interval_obj = Interval.objects.get(rule_item=rule_item_obj)
            return redirect('rule', pk=rule_item_obj.pk)


def delete_strategy(request,pk):
    rule_item_obj = Rule_Item.objects.get(pk=pk)
    rule_item_obj.delete()
    return redirect('strategies_page')

def rule_item(request,pk):
    if request.method == 'POST':
        pass
    else: #when we have GET we create the rule item

        rule_item_obj = Rule_Item.objects.get(pk=pk)
        filter_obj = Filter.objects.get(rule_item=rule_item_obj) #we use "get" instead of "filter" because when only one result is returned we must use "get"
        condition_obj = Condition.objects.get(rule_item=rule_item_obj)
        condition_item_obj = list(ConditionItem.objects.filter(condition=condition_obj))
        action_obj = Action.objects.get(rule_item=rule_item_obj)
        interval_obj = Interval.objects.get(rule_item=rule_item_obj)


        condition_item_obj_form = []
        filter_item_obj = None
        #check which filter is applied
        if filter_obj.filter_type == 'D':
            filter_type_form = FilterForm(instance=filter_obj)

        elif filter_obj.filter_type == 'S':
            filter_item_obj = FilterStatus.objects.get(filter=filter_obj)
            filter_type_form = FilterStatusForm(instance=filter_item_obj)

        elif filter_obj.filter_type == 'I':
            filter_item_obj = FilterId.objects.get(filter=filter_obj)
            filter_type_form = FilterIdForm(instance=filter_item_obj)

        filter_form = FilterForm(instance=filter_obj)
        condition_form = ConditionForm(instance=condition_obj)
        condition_item_form = list(ConditionItemForm(instance=condition_item_ins) for condition_item_ins in condition_item_obj)
        action_form = ActionForm(instance=action_obj)
        interval_form = IntervalForm(instance=interval_obj)
        #TODO since filter_item_obj is a list we will get a list of items, and for each item we needa forminstance,
        # so in the template we use for loop to acces the forms and in the viewvs we simply put "filter_item_form" as a list

        #combine condition item forms and object at a dict to access them at the same time in a for loop in template
        for ind, obj in enumerate(condition_item_obj):
            obj_form = condition_item_form[ind]
            condition_item_obj_form.append({'obj':obj,'form':obj_form})
        context = {
            'rule_item':rule_item_obj,
            'filter_form':filter_form,
            'filter_obj':filter_obj, #we get this to check if the filter is confirmed
            'filter_type_obj':filter_item_obj,
            'filter_type_form':filter_type_form,
            'condition_form':condition_form,
            'condition_obj':condition_obj,
            'condition_item_form':condition_item_form,
            'action_obj':action_obj,
            'action_form':action_form,
            'condition_item':condition_item_obj_form,
            'interval_form':interval_form,
            'interval_obj':interval_obj,
        }

        return render(request,'rules_app/rule.html', context)

def list_rules(request):
    pass