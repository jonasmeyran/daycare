import unittest
from entities import Child, Classroom
from datetime import date

class TestBase(unittest.TestCase):
    def setUp(self):
        self.child1 = Child(name='Aiden Chan', date_of_birth=date(2023, 7, 26))
        self.child1.add_infant(classroom='INFANT1', start_date=date(2024, 8, 6), transition_date=date(2024, 8, 8))
        self.child1.add_toddler(classroom='TODDLER1', start_date=date(2024, 8, 8), transition_date=date(2024, 8, 10))

        self.child2 = Child(name='Emma Martinez', date_of_birth=date(2023, 4, 1))
        self.child2.add_infant(classroom='INFANT1', start_date=date(2024, 8, 4), transition_date=date(2024, 8, 8))
        self.child2.add_toddler(classroom='TODDLER1', start_date=date(2024, 8, 8), transition_date=date(2024, 8, 10))

        self.child_A = Child(name='Alex', date_of_birth=date(2023, 5, 12))
        self.child_B = Child(name='Ben', date_of_birth=date(2023, 8, 13))
        self.child_C = Child(name='Charles', date_of_birth=date(2023, 4, 18))
        self.child_D = Child(name='David', date_of_birth=date(2023, 2, 1))

        self.child_A.add_infant(classroom='INFANT1', start_date=date(2024, 1, 1), transition_date=date(2024, 11, 14))
        self.child_B.add_toddler(classroom='TODDLER1', start_date=date(2024, 12, 17), transition_date=date(2026, 4, 12))
        self.child_C.add_toddler(classroom='TODDLER1', start_date=date(2024, 7, 22), transition_date=date(2025, 12, 22))
        self.child_D.add_toddler(classroom='TODDLER1', start_date=date(2024, 4, 3), transition_date=date(2025, 12, 3))

class TestClassroom(TestBase):
    def setUp(self):
        super().setUp()
        self.classroomI1 = Classroom(name='INFANT1', max_size=10, 
                                     entrance_min_age=6, entrance_normal_age=6, 
                                     transition_normal_age=18, transition_max_age=21)
        self.classroomT1 = Classroom(name='TODDLER1', max_size=16, 
                                     entrance_min_age=15, entrance_normal_age=18, 
                                     transition_normal_age=30, transition_max_age=34)
        
    def _setup_test_update_categories_distribution(self):
        self.classroomI1.create_date_dict(start_date=date(2024,1,1), end_date=date(2024,11,14))
        self.classroomI1.add_child(self.child_A)
        self.classroomI1.update_categories_distribution()

        self.classroomT1.create_date_dict(start_date=date(2024,4,3), end_date=date(2025,12,22))
        self.classroomT1.add_child(self.child_B)
        self.classroomT1.add_child(self.child_C)
        self.classroomT1.add_child(self.child_D)

        self.classroomT1.update_categories_distribution()

    # Calendar and child management

    def test_create_date_dict(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,6), end_date=date(2024,8,9))
        date_dict = {date(2024,8,6): [], date(2024,8,7): [], date(2024,8,8): [], date(2024,8,9): []}
        self.assertEqual(self.classroomI1.date_dict, date_dict)

    def test_delete_date_dict(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,6), end_date=date(2024,8,9))
        self.classroomI1.delete_date(date(2024,8,6))
        date_dict = {date(2024,8,7): [], date(2024,8,8): [], date(2024,8,9): []}
        self.assertEqual(self.classroomI1.date_dict, date_dict)

    def test_add_child(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,4), end_date=date(2024,8,12))
        self.classroomT1.create_date_dict(start_date=date(2024,8,4), end_date=date(2024,8,12))

        self.classroomI1.add_child(child=self.child1)
        self.classroomT1.add_child(child=self.child1)

        date_dict_I1 = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): ['Aiden Chan'], 
                        date(2024,8,7): ['Aiden Chan'], date(2024,8,8): [], 
                        date(2024,8,9): [], date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}
        
        date_dict_T1 = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): [], 
                        date(2024,8,7): [], date(2024,8,8): ['Aiden Chan'], date(2024,8,9): ['Aiden Chan'],
                        date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}

        self.assertEqual(self.classroomI1.date_dict, date_dict_I1)
        self.assertEqual(self.classroomT1.date_dict, date_dict_T1)

        self.assertEqual(self.classroomI1.list_of_children, [self.child1])

        self.classroomI1.add_child(child=self.child2)
        self.classroomT1.add_child(child=self.child2)

        date_dict_I1 = {date(2024,8,4): ['Emma Martinez'], date(2024,8,5): ['Emma Martinez'], date(2024,8,6): ['Aiden Chan', 'Emma Martinez'], 
                        date(2024,8,7): ['Aiden Chan', 'Emma Martinez'], date(2024,8,8): [], 
                        date(2024,8,9): [], date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}
        
        date_dict_T1 = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): [], 
                        date(2024,8,7): [], date(2024,8,8): ['Aiden Chan', 'Emma Martinez'], date(2024,8,9): ['Aiden Chan', 'Emma Martinez'],
                        date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}

        self.assertEqual(self.classroomI1.date_dict, date_dict_I1)
        self.assertEqual(self.classroomT1.date_dict, date_dict_T1)

        self.assertEqual(self.classroomI1.list_of_children, [self.child1, self.child2])

        
    def test_delete_child(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,4), end_date=date(2024,8,12))
        self.classroomI1.add_child(child=self.child1)
        self.classroomI1.add_child(child=self.child2)

        self.classroomI1.delete_child(self.child2)

        date_dict_I1 = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): ['Aiden Chan'], 
                        date(2024,8,7): ['Aiden Chan'], date(2024,8,8): [], 
                        date(2024,8,9): [], date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}
        
        self.assertEqual(self.classroomI1.date_dict, date_dict_I1)
        self.assertEqual(self.classroomI1.list_of_children, [self.child1])
    
    # Vacancy calculation

    def test_vacant_places_on_date(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,6), end_date=date(2024,8,12))
        self.classroomI1.add_child(child=self.child1)

        vacant_places = self.classroomI1.vacant_places_on_date(date(2024,8,7))
        self.assertEqual(vacant_places, 9)

    def test_compute_vacant_places_rate_on_date(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,6), end_date=date(2024,8,12))
        self.classroomI1.add_child(child=self.child1)
        
        vacant_places_rate_1 = self.classroomI1.compute_vacant_places_rate_on_date(date(2024,8,7))
        vacant_places_rate_2 = self.classroomI1.compute_vacant_places_rate_on_date(date(2024,8,9))
        
        self.assertEqual(vacant_places_rate_1, 90)
        self.assertEqual(vacant_places_rate_2, 100)

    def test_compute_vacant_places_rate_on_period(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,6), end_date=date(2024,8,12))
        self.classroomI1.add_child(child=self.child1)
        
        vacant_places_rate1 = self.classroomI1.compute_vacant_places_rate_on_period(date(2024,8,6), date(2024,8,11))
        vacant_places_rate2 = self.classroomI1.compute_vacant_places_rate_on_period(date(2024,8,6), date(2024,8,8))
        
        self.assertEqual(vacant_places_rate1, 290/3)
        self.assertEqual(vacant_places_rate2, 280/3)

    def test_vacant_places_intervals(self):
        self.classroomI1.create_date_dict(start_date=date(2024,8,2), end_date=date(2024,8,10))
        for _ in range(9):
            self.classroomI1.add_child(self.child2)
        self.classroomI1.add_child(self.child1)

        vacant_positions_interval = [(date(2024, 8, 2), date(2024, 8, 3), 10),
                                     (date(2024, 8, 4), date(2024, 8, 5), 1), 
                                     (date(2024, 8, 8), date(2024, 8, 10), 10)]
        self.assertEqual(self.classroomI1.vacant_places_intervals(), vacant_positions_interval)

    # Child categorization

    def test_categorize_start_and_transition_age(self):
        self.assertEqual(self.classroomI1.categorize_start_age(self.child_A), 'A')
        self.assertEqual(self.classroomI1.categorize_transition_age(self.child_A), 'A')

        self.assertEqual(self.classroomT1.categorize_start_age(self.child_B), 'B')
        self.assertEqual(self.classroomT1.categorize_transition_age(self.child_B), 'B')
        
        self.assertEqual(self.classroomT1.categorize_start_age(self.child_C), 'C')
        self.assertEqual(self.classroomT1.categorize_transition_age(self.child_C), 'C')
        
        self.assertEqual(self.classroomT1.categorize_start_age(self.child_D), 'D')
        self.assertEqual(self.classroomT1.categorize_transition_age(self.child_D), 'D')
    
    def test_update_categories_distribution(self):
        self._setup_test_update_categories_distribution()

        self.assertEqual(self.classroomI1.start_categories, {"A": 1, "B": 0, "C": 0, "D": 0})
        self.assertEqual(self.classroomI1.transition_categories, {"A": 1, "B": 0, "C": 0, "D": 0})

        self.assertEqual(self.classroomT1.start_categories, {"A": 0, "B": 1, "C": 1, "D": 1})
        self.assertEqual(self.classroomT1.transition_categories, {"A": 0, "B": 1, "C": 1, "D": 1})

    # Validation

    def test_meets_the_stardards(self):
        self._setup_test_update_categories_distribution()
        self.assertEqual(self.classroomI1.meets_the_stardards(), True)
        self.assertEqual(self.classroomT1.meets_the_stardards(), False)

if __name__ == '__main__':
    unittest.main()