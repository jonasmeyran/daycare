from entities import Child
from datetime import date, timedelta
from typing import Any
from typing import Literal


class Classroom:
    def __init__(self, name: str, max_size: int, 
                 entrance_min_age: int, entrance_normal_age: int, 
                 transition_normal_age: int, transition_max_age: int) -> None:
        self.name = name
        self.max_size = max_size
        self.entrance_min_age = entrance_min_age
        self.entrance_normal_age = entrance_normal_age
        self.transition_normal_age = transition_normal_age
        self.transition_max_age = transition_max_age
        self.date_dict = {}  # composition of the classroom for each date
        self.start_categories = {"A": 0, "B": 0, "C": 0, "D": 0}
        self.transition_categories = {"A": 0, "B": 0, "C": 0, "D": 0}
        self.list_of_children = []

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    # Calendar and child management

    def create_date_dict(self, start_date, end_date):
        current_date = start_date
        while current_date <= end_date:
            self.date_dict[current_date] = []
            current_date += timedelta(days=1)
    
    def delete_date(self, date: date):
        del self.date_dict[date]

    def add_child(self, child: Child):
        for stage in [child.infant, child.toddler, child.preschool]:
            
            if stage['classroom'] == self.name:
                self.list_of_children.append(child)

                current_date = max(stage['start_date'], min(self.date_dict))
                end_date = min(stage['transition_date'] - timedelta(days=1), max(self.date_dict))
                
                while current_date <= end_date: 
                    self.date_dict[current_date].append(child.name)
                    current_date += timedelta(days=1)

                break

    def delete_child(self, child: Child):
        if child in self.list_of_children:
            self.list_of_children.remove(child)
            
            for date in self.date_dict:
                if child.name in self.date_dict[date]:
                    self.date_dict[date].remove(child.name)

    # Vacancy calculation

    def compute_vacant_places_on_date(self, date: date) -> int:
        nb_children = len(self.date_dict[date])
        return self.max_size - nb_children
    
    def compute_vacant_places_on_period(self, start_date: date, end_date: date) -> int:
        vacant_places = 0
        
        current_date = start_date
        while current_date <= end_date:
            vacant_places += self.compute_vacant_places_on_date(current_date)
            current_date += timedelta(days=1)

        return vacant_places

    def compute_vacant_places_rate_on_date(self, date: date) -> float:
        nb_children = len(self.date_dict[date])
        return 100 * (self.max_size - nb_children) / self.max_size
    
    def compute_vacant_places_rate_on_period(self, start_date: date, end_date: date) -> float:
        vacant_places_rate = 0
        difference = end_date - start_date
        
        current_date = start_date
        while current_date <= end_date:
            vacant_places_rate += self.compute_vacant_places_rate_on_date(current_date)
            current_date += timedelta(days=1)

        return vacant_places_rate / (difference.days + 1)
    
    def vacant_places_intervals(self) -> list:
        intervals = []
        start_date = None
        current_vacancies = None

        for current_date in self.date_dict.keys():
            vacancies = self.max_size - len(self.date_dict[current_date])
            if vacancies == current_vacancies:
                continue
            
            if current_vacancies is not None and current_vacancies > 0:
                intervals.append((start_date, current_date - timedelta(days=1), current_vacancies))

            start_date = current_date
            current_vacancies = vacancies
        
        if current_vacancies > 0:
            intervals.append((start_date, current_date, current_vacancies))

        return intervals
    
    # Child categorization

    def categorize_start_age(self, child: Child) -> Literal['A', 'B', 'C', 'D']:
        for stage in [child.infant, child.toddler, child.preschool]:
            if stage['classroom'] == self.name:
                start_date = stage['start_date']
                break
        
        start_age = child.compute_age_in_months(start_date)

        if start_age < self.entrance_min_age: return 'D'
        elif start_age < self.entrance_normal_age - 2: return 'C'
        elif start_age < self.entrance_normal_age - 1: return 'B'
        else: return 'A'

    def categorize_transition_age(self, child: Child) -> Literal['A', 'B', 'C', 'D']:
        for stage in [child.infant, child.toddler, child.preschool]:
            if stage['classroom'] == self.name:
                transition_date = stage['transition_date']
                break

        transition_age = child.compute_age_in_months(transition_date)

        if transition_age > self.transition_max_age - 1: return 'D'
        elif transition_age > self.transition_normal_age + 1: return 'C'
        elif transition_age > self.transition_normal_age: return 'B'
        else: return 'A'

    def update_categories_distribution(self):
        for child in self.list_of_children:
            self.start_categories[self.categorize_start_age(child)] += 1
            self.transition_categories[self.categorize_transition_age(child)] += 1

    # Validation

    def meets_the_stardards(self):
        return self.start_categories["D"] == 0 and self.transition_categories["D"] == 0
            