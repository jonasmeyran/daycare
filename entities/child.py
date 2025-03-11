from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Any

class Child:
    def __init__(self, name: str, date_of_birth: date):
        self.name = name
        self.date_of_birth = date_of_birth
        self.infant = {"classroom": None, "start_date": None, "transition_date": None}
        self.toddler = {"classroom": None, "start_date": None, "transition_date": None}
        self.preschool = {"classroom": None, "start_date": None, "transition_date": None}

    def modify_date_of_birth(self, date: date):
        self.date_of_birth = date

    def add_infant(self, classroom: str, start_date: date, transition_date: date):
        self.infant = {"classroom": classroom, "start_date": start_date, "transition_date": transition_date}
    
    def add_toddler(self, classroom: str, start_date: date, transition_date: date):
        self.toddler = {"classroom": classroom, "start_date": start_date, "transition_date": transition_date}

    def add_preschool(self, classroom: str, start_date: date, transition_date: date):
        self.preschool = {"classroom": classroom, "start_date": start_date, "transition_date": transition_date}
    
    def compute_age_in_months(self, current_date: date) -> int:
        delta = relativedelta(current_date, self.date_of_birth)
        return delta.years * 12 + delta.months

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)