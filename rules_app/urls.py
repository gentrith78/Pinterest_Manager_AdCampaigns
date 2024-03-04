from django.urls import path

from . import views

urlpatterns = [
    path('',views.dashboard,name = 'strategies_page'),
    path('strategies',views.dashboard,name = 'strategies_page'),
    path('add-rule/<pk>',views.add_strategy,name="add_rule"),
    path('manage-rule/<pk>',views.rule_item,name="rule"),
    path('delete-rule/<pk>',views.delete_strategy,name="delete_rule"),
    path('p-a-rule/<pk>/<st>',views.pause_activate_strategy,name="p_a_rule"), #pause activate rule
    path('filter-add/<int:pk>',views.add_filter,name="filter_add"),
    path('filter-status-process/<pk>',views.confirm_filter_status,name="filter_status_process"),
    path('filter-status-delete/<pk>',views.delete_filter_status,name="filter_status_delete"),
    path('filter-id-process/<pk>', views.confirm_filter_id, name="filter_id_process"),
    path('filter-id-delete/<pk>', views.delete_filter_id, name="filter_id_delete"),
    path('condition-add/<pk>', views.add_conditionItem, name="condition_add"),
    path('condition-update-op/<pk>', views.update_match_operator, name="operator_update"),
    path('condition-confirm/<pk>/<id>', views.confirm_conditionItem, name="condition_confirm"),
    path('condition-delete/<pk>/<id>', views.delete_conditionItem, name="condition_delete"),
    path('action-confirm/<pk>', views.action_confirm, name="action_confirm"),
    path('action-delete/<pk>', views.action_delete, name="action_delete"),
    path('interval-confirm/<pk>', views.confirm_interval, name="interval_confirm"),

]


