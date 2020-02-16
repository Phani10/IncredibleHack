"""
@author: Phani Kumar Koratamaddi
This script is to test insert_to_mysql.py file
"""
from unittest import TestCase

import insert_to_mysql


class TestInsertToMySql(TestCase):
    """
    This class takes data source input (identifier) and tests if the x1-x5 columns has null values or
    if they are non-float values. CIN must not be null. 
    """

    @classmethod
    def setUpClass(cls):
        """function to load test df and output df frame.
         It runs once only"""

        cls.instance = insert_to_mysql.MysqlIo()

    @classmethod
    def tearDownClass(cls):
        """this function runs once after execution of all functions"""
        pass

    def test_read_from_db(self):
        """
        Function to test read_from_db
        :return: assertion
        """
        test_df = self.instance.read_from_db()
        test_df.drop_duplicates(inplace=True)
        self.assertEqual(test_df.shape[1], 23)
        self.assertEqual(test_df['CIN'].isnull().sum(), 0)
        self.assertEqual(test_df[['x1', 'x2', 'x3', 'x4', 'x5']].isnull().sum().sum(), 0)
        self.assertEqual(all(test_df[['x1', 'x2', 'x3', 'x4', 'x5']].dtypes == 'float64'), True)
