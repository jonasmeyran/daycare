from entities import Child, Classroom
from datetime import date
from typing import Any

class Daycare:
    def __init__(self) -> None:
        self.classrooms = {
            'INFANT1': Classroom(name='INFANT1', max_size=10, 
                                 entrance_min_age=6, entrance_normal_age=6, 
                                 transition_normal_age=18, transition_max_age=21),
            'INFANT2': Classroom(name='INFANT2', max_size=10, 
                                 entrance_min_age=6, entrance_normal_age=6, 
                                 transition_normal_age=18, transition_max_age=21),
            'TODDLER1': Classroom(name='TODDLER1', max_size=15,
                                  entrance_min_age=15, entrance_normal_age=18, 
                                  transition_normal_age=30, transition_max_age=34),
            'TODDLER3': Classroom(name='TODDLER3', max_size=15,
                                  entrance_min_age=15, entrance_normal_age=18, 
                                  transition_normal_age=30, transition_max_age=34),
            'TODDLER4': Classroom(name='TODDLER4', max_size=15,
                                  entrance_min_age=15, entrance_normal_age=18, 
                                  transition_normal_age=30, transition_max_age=34),
            'PRESCHOOL1': Classroom(name='PRESCHOOL1', max_size=16, 
                                    entrance_min_age=26, entrance_normal_age=30, 
                                    transition_normal_age=60, transition_max_age=60),                      
            'PRESCHOOL2': Classroom(name='PRESCHOOL2', max_size=16, 
                                    entrance_min_age=26, entrance_normal_age=30, 
                                    transition_normal_age=60, transition_max_age=60),
            'PRESCHOOL3': Classroom(name='PRESCHOOL3', max_size=16, 
                                    entrance_min_age=26, entrance_normal_age=30, 
                                    transition_normal_age=60, transition_max_age=60), 
            'PRESCHOOL4': Classroom(name='PRESCHOOL4', max_size=16, 
                                    entrance_min_age=26, entrance_normal_age=30, 
                                    transition_normal_age=60, transition_max_age=60), 
        }

        self.start_categories = {"A": 0, "B": 0, "C": 0, "D": 0}
        self.transition_categories = {"A": 0, "B": 0, "C": 0, "D": 0}


    def get_classroom(self, name: str):
        return self.classrooms.get(name)
    
    # Calendar and child management

    def create_date_dicts(self, start_date: date, end_date: date):
        for classrooms in self.classrooms.values():
            classrooms.create_date_dict(start_date, end_date)

    def delete_date(self, date: date):
       for classroom in self.classrooms.values():
            classroom.delete_date(date)

    def add_child(self, child: Child):
        for classroom in self.classrooms.values():
            classroom.add_child(child)

    def delete_child(self, child: Child):
        for classroom in self.classrooms.values():
            classroom.delete_child(child)

    # Vacancy calculation
    
    def compute_vacant_places_rate_on_period(self, start_date: date, end_date: date) -> float:
        vacant_places = 0
        difference = end_date - start_date
        
        total_size = sum(classroom.max_size for classroom in self.classrooms.values())
        
        for classroom in self.classrooms.values():
            vacant_places += classroom.compute_vacant_places_on_period(start_date, end_date)

        return 100 * vacant_places / (total_size * (difference.days + 1))
    
    def compute_vacant_places_rate_on_period_stage(self, stage, start_date: date, end_date: date) -> float:
        total_size_stage = 0
        vacant_places = 0
        difference = end_date - start_date
        
        for classroom in self.classrooms.values():
            if stage in classroom.name:
                total_size_stage += classroom.max_size 
                vacant_places += classroom.compute_vacant_places_on_period(start_date, end_date)
        
        return 100 * vacant_places / (total_size_stage * (difference.days + 1))

    # Child categorization

    def update_categories_distributions(self):
        for classroom in self.classrooms.values():
            classroom.update_categories_distribution()
            
            self.start_categories = {key: self.start_categories[key] + classroom.start_categories[key] 
                                             for key in self.start_categories}
            self.transition_categories = {key: self.transition_categories[key] + classroom.transition_categories[key] 
                                             for key in self.transition_categories}

    # Validation

    def meets_the_stardards(self):
        return self.start_categories["D"] == 0 and self.transition_categories["D"] == 0
    
    # Cost

    """def compute_configuration_cost(self, start_date: date, end_date: date) -> float:
        if not self.meets_the_stardards():
            return float("inf")

        lambda_vpr = 1
        lambda_A = 1
        lambda_B = 2
        lambda_C = 3

        vacant_place_rate = self.compute_vacant_places_rate_on_period(start_date, end_date)
        A_start, B_start, C_start, _ = self.start_categories.values
        A_transition, B_transition, C_transition, _ = self.transition_categories.values     

        return lambda_vpr * vacant_place_rate + lambda_A * (A_start + A_transition) + lambda_B * (B_start + B_transition) + lambda_C * (C_start + C_transition)
"""