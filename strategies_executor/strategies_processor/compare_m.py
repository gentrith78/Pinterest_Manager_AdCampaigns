
class Comparison:
    ConditionItem_variable:float
    ConditionItem_desired_value: float
    Received_Value: float
    operator:str


def compare(comparison_obj):
    if comparison_obj.operator == 'E':
        return comparison_obj.ConditionItem_inputted_value == comparison_obj.Received_Value
    if comparison_obj.operator == 'NE':
        return comparison_obj.ConditionItem_inputted_value != comparison_obj.Received_Value
    if comparison_obj.operator == 'GT':
        return comparison_obj.ConditionItem_inputted_value > comparison_obj.Received_Value
    if comparison_obj.operator == 'GTE':
        return comparison_obj.ConditionItem_inputted_value >= comparison_obj.Received_Value
    if comparison_obj.operator == 'LT':
        return comparison_obj.ConditionItem_inputted_value < comparison_obj.Received_Value
    if comparison_obj.operator == 'LTE':
        return comparison_obj.ConditionItem_inputted_value > comparison_obj.Received_Value
