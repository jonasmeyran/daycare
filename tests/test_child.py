from entities import Child
from datetime import date
import unittest


class TestChild(unittest.TestCase):
    def setUp(self):
        self.child = Child(name='Aiden Chan', date_of_birth=date(2023, 7, 26))

    def test_modify_date_of_birth(self):
        self.child.modify_date_of_birth(date(2023, 8, 26))
        self.assertEqual(self.child.date_of_birth, date(2023, 8, 26))

    def test_add_infant(self):
        self.child.add_infant(classroom='INFANT1', start_date=date(2024, 8, 6), transition_date=date(2025, 1, 6))
        self.assertEqual(self.child.infant, 
                         {"classroom": 'INFANT1', "start_date": date(2024, 8, 6), "transition_date": date(2025, 1, 6)})
        
    def test_compute_age_in_months(self):
        age_in_month1 = self.child.compute_age_in_months(date(2024, 9, 8))
        age_in_month2 = self.child.compute_age_in_months(date(2024, 9, 26))
        age_in_month3 = self.child.compute_age_in_months(date(2024, 9, 29))
        
        self.assertEqual(age_in_month1, 13)
        self.assertEqual(age_in_month2, 14)
        self.assertEqual(age_in_month3, 14)


if __name__ == '__main__':
    unittest.main()