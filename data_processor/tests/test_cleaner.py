import unittest
import pandas as pd
import numpy as np
from src.cleaner import DataCleaner

class TestDataCleaner(unittest.TestCase):
    def setUp(self):
        data = {
            'A': [1, 2, 2, 3, np.nan],
            'B': ['a', 'b', 'b', 'c', 'd'],
            'C': [1.1, 2.2, 3.3, 4.4, 5.5],
            'D': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05']
        }
        self.df = pd.DataFrame(data)
        self.cleaner = DataCleaner(self.df)

    def test_remove_duplicates(self):
        self.cleaner.remove_duplicates()
        self.assertEqual(len(self.cleaner.data), 4)

    def test_handle_missing_values_mean(self):
        self.cleaner.handle_missing_values(strategy='mean', columns=['A'])
        self.assertFalse(self.cleaner.data['A'].isnull().any())
        self.assertEqual(self.cleaner.data['A'].iloc[-1], 2.0)

    def test_handle_missing_values_median(self):
        self.cleaner.handle_missing_values(strategy='median', columns=['A'])
        self.assertFalse(self.cleaner.data['A'].isnull().any())
        self.assertEqual(self.cleaner.data['A'].iloc[-1], 2.0)

    def test_normalize_column_names(self):
        self.cleaner.data.columns = ['Column A', 'Column B', 'Column C', 'Column D']
        self.cleaner.normalize_column_names()
        self.assertListEqual(list(self.cleaner.data.columns), ['column_a', 'column_b', 'column_c', 'column_d'])

    def test_convert_data_types(self):
        type_dict = {'A': 'float', 'B': 'category', 'C': 'int'}
        self.cleaner.convert_data_types(type_dict)
        self.assertEqual(self.cleaner.data['A'].dtype, 'float64')
        self.assertEqual(self.cleaner.data['B'].dtype, 'category')
        self.assertEqual(self.cleaner.data['C'].dtype, 'int64')

    def test_remove_outliers_zscore(self):
        self.cleaner.data = pd.DataFrame({'A': [1, 2, 3, 4, 100]})
        self.cleaner.remove_outliers(['A'], method='zscore', threshold=2)
        self.assertEqual(len(self.cleaner.data), 4)

    def test_remove_outliers_iqr(self):
        self.cleaner.data = pd.DataFrame({'A': [1, 2, 3, 4, 100]})
        self.cleaner.remove_outliers(['A'], method='iqr')
        self.assertEqual(len(self.cleaner.data), 4)

    def test_normalize_data_minmax(self):
        self.cleaner.normalize_data(['C'], method='minmax')
        self.assertEqual(self.cleaner.data['C'].min(), 0)
        self.assertEqual(self.cleaner.data['C'].max(), 1)

    def test_normalize_data_zscore(self):
        self.cleaner.normalize_data(['C'], method='zscore')
        self.assertAlmostEqual(self.cleaner.data['C'].mean(), 0, places=10)
        self.assertAlmostEqual(self.cleaner.data['C'].std(), 1, places=10)

    def test_handle_categorical_data_onehot(self):
        self.cleaner.handle_categorical_data(['B'], method='onehot')
        self.assertIn('B_a', self.cleaner.data.columns)
        self.assertIn('B_b', self.cleaner.data.columns)
        self.assertIn('B_c', self.cleaner.data.columns)
        self.assertIn('B_d', self.cleaner.data.columns)

    def test_handle_categorical_data_label(self):
        self.cleaner.handle_categorical_data(['B'], method='label')
        self.assertEqual(set(self.cleaner.data['B']), {0, 1, 2, 3})

    def test_clean_text_data(self):
        self.cleaner.data['E'] = ['Hello, World!', 'Test 123', 'Python & Data']
        self.cleaner.clean_text_data(['E'])
        self.assertListEqual(list(self.cleaner.data['E']), ['hello world', 'test 123', 'python  data'])

    def test_format_dates(self):
        self.cleaner.format_dates(['D'])
        self.assertEqual(self.cleaner.data['D'].dtype, 'datetime64[ns]')

if __name__ == '__main__':
    unittest.main()