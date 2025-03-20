import unittest
from entities import Child, Daycare
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

class TestDaycare(TestBase):
    def setUp(self):
        super().setUp()
        self.daycare = Daycare()
        self.classrooms = self.daycare.classrooms

    def _setup_test_update_categories_distribution(self):
        child_A_B_C = Child(name='Aaron', date_of_birth=date(2023, 5, 6))
        child_A_B_C.add_infant(classroom='INFANT1', start_date=date(2023, 12, 8), transition_date=date(2024, 9, 7))
        child_A_B_C.add_toddler(classroom='TODDLER1', start_date=date(2024, 9, 7), transition_date=date(2025, 8, 3))
        child_A_B_C.add_preschool(classroom='PRESCHOOL1', start_date=date(2025, 8, 3), transition_date=date(2027, 5, 6))

        self.daycare.create_date_dicts(start_date=date(2023, 12, 8), end_date=date(2027, 5, 6))
        self.daycare.add_child(child_A_B_C)
        self.daycare.update_categories_distributions()

    # Calendar and child management

    def test_create_date_dicts(self):
        self.daycare.create_date_dicts(start_date=date(2024,8,6), end_date=date(2024,8,9))
        date_dict = {date(2024,8,6): [], date(2024,8,7): [], date(2024,8,8): [], date(2024,8,9): []}
        
        for classroom in self.classrooms.values():
            self.assertEqual(classroom.date_dict, date_dict)

    def test_delete_date(self):
        self.daycare.create_date_dicts(start_date=date(2024,8,6), end_date=date(2024,8,9))
        self.daycare.delete_date(date(2024,8,6))
        date_dict = {date(2024,8,7): [], date(2024,8,8): [], date(2024,8,9): []}
        
        for classroom in self.classrooms.values():
            self.assertEqual(classroom.date_dict, date_dict)

    def test_add_child(self):
        self.daycare.create_date_dicts(start_date=date(2024,8,4), end_date=date(2024,8,12))
        self.daycare.add_child(self.child1)

        date_dict_I1 = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): ['Aiden Chan'], 
                        date(2024,8,7): ['Aiden Chan'], date(2024,8,8): [], 
                        date(2024,8,9): [], date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}
        
        date_dict_T1 = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): [], 
                        date(2024,8,7): [], date(2024,8,8): ['Aiden Chan'], date(2024,8,9): ['Aiden Chan'],
                        date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}
        
        date_dict_P1 = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): [], 
                        date(2024,8,7): [], date(2024,8,8): [], date(2024,8,9): [],
                        date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}
            
        infant_1 = self.daycare.get_classroom('INFANT1')
        toddler_1 = self.daycare.get_classroom('TODDLER1')
        preschool_1 = self.daycare.get_classroom('PRESCHOOL1')

        self.assertEqual(infant_1.date_dict, date_dict_I1)
        self.assertEqual(toddler_1.date_dict, date_dict_T1)
        self.assertEqual(preschool_1.date_dict, date_dict_P1)

    def test_delete_child(self):
        self.daycare.create_date_dicts(start_date=date(2024,8,4), end_date=date(2024,8,12))
        self.daycare.add_child(self.child1)
        self.daycare.delete_child(self.child1)

        date_dict = {date(2024,8,4): [], date(2024,8,5): [], date(2024,8,6): [], 
                        date(2024,8,7): [], date(2024,8,8): [], date(2024,8,9): [],
                        date(2024,8,10): [], date(2024,8,11): [], date(2024,8,12): []}
        
        for classroom in self.classrooms.values():
            self.assertEqual(classroom.date_dict, date_dict)

    # Vacancy calculation

    def test_compute_vacant_places_rate_on_period(self):
        self.daycare.create_date_dicts(start_date=date(2024,8,4), end_date=date(2024,8,12))
        self.daycare.add_child(self.child1)
        self.daycare.add_child(self.child2)
        
        vacant_places_rate = self.daycare.compute_vacant_places_rate_on_period(start_date=date(2024,8,4), end_date=date(2024,8,12))
        
        self.assertEqual(vacant_places_rate, 100 * 1151/1161)

    def test_compute_vacant_places_rate_on_period_stage(self):
        self.daycare.create_date_dicts(start_date=date(2024,8,4), end_date=date(2024,8,12))
        self.daycare.add_child(self.child1)
        self.daycare.add_child(self.child2)
        
        vacant_places_rate = self.daycare.compute_vacant_places_rate_on_period_stage(stage= 'INFANT', start_date=date(2024,8,4), end_date=date(2024,8,12))
        
        self.assertEqual(vacant_places_rate, 100 * 174/180)

    # Child categorization

    def test_update_categories_distributions(self):
        self._setup_test_update_categories_distribution()

        self.assertEqual(self.daycare.get_classroom('INFANT1').start_categories, {"A": 1, "B": 0, "C": 0, "D": 0})
        self.assertEqual(self.daycare.get_classroom('INFANT2').start_categories, {"A": 0, "B": 0, "C": 0, "D": 0})
        self.assertEqual(self.daycare.get_classroom('TODDLER1').start_categories, {"A": 0, "B": 1, "C": 0, "D": 0})
        self.assertEqual(self.daycare.get_classroom('PRESCHOOL1').start_categories, {"A": 0, "B": 0, "C": 1, "D": 0})

        self.assertEqual(self.daycare.start_categories, {"A": 1, "B": 1, "C": 1, "D": 0})

    # Validation

    def test_meets_the_standards(self):
        self._setup_test_update_categories_distribution()

        self.assertEqual(self.daycare.meets_the_stardards(), True)


if __name__ == '__main__':
    unittest.main()