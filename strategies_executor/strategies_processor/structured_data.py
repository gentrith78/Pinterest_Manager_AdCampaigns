from dataclasses import dataclass

"""
a module that will have structured data
"""

@dataclass
class CampaignItem:
        id: int
        name: str
        status: str
        lifetime_spend_cap: int
        daily_spend_cap: int

@dataclass
class Comparison:
    ConditionItem_variable:float
    ConditionItem_inputted_value: float
    Received_Value: float
    operator:str
    match: bool = False
