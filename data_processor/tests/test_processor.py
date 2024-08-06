import unittest
import asyncio
import os
import tempfile
import pandas as pd
from src.processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_collect_and_clean_data(self):
        async def run_test():
            # Create a test CSV file
            test_df = pd.DataFrame({
                'A': [1, 2, 2, 3, 4],
                'B': ['a', 'b', 'b', 'c', 'd'],
                'C': [1.1, 2.2, 3.3, 4.4, 5.5]
            })
            input_file = os.path.join(self.temp_dir, 'input.csv')
            test_df.to_csv(input_file, index=False)

            output_file = os.path.join(self.temp_dir, 'output.csv')

            config = {
                'source': {
                    'source_type': 'csv',
                    'file_path': input_file
                },
                'cleaning_operations': {
                    'remove_duplicates': {},
                    'handle_missing_values': {'strategy': 'mean'},
                    'normalize_data': {'columns': ['C'], 'method': 'minmax'}
                },
                'output': {
                    'output_type': 'csv',
                    'file_path': output_file
                }
            }

            await self.processor.collect_data(**config['source'])
            self.assertIsNotNone(self.processor.cleaner.data)
            self.assertEqual(len(self.processor.cleaner.data), 5)

            self.processor.clean_data(config['cleaning_operations'])
            self.assertEqual(len(self.processor.cleaner.data), 4)  # One duplicate removed
            self.assertEqual(self.processor.cleaner.data['C'].min(), 0)
            self.assertEqual(self.processor.cleaner.data['C'].max(), 1)

            self.processor.save_data(**config['output'])
            self.assertTrue(os.path.exists(output_file))

            # Verify the output
            output_df = pd.read_csv(output_file)
            self.assertEqual(len(output_df), 4)
            self.assertListEqual(list(output_df.columns), ['A', 'B', 'C'])

        asyncio.run(run_test())

    @unittest.skip("Requires web server setup")
    def test_collect_from_web_and_process(self):
        async def run_test():
            config = {
                'source': {
                    'source_type': 'web',
                    'url': 'http://example.com/data'
                },
                'cleaning_operations': {
                    'clean_text_data': {'columns': ['text_column']},
                    'handle_categorical_data': {'columns': ['category_column'], 'method': 'onehot'}
                },
                'output': {
                    'output_type': 'json',
                    'file_path': os.path.join(self.temp_dir, 'output.json')
                }
            }

            await self.processor.collect_data(**config['source'])
            self.assertIsNotNone(self.processor.cleaner.data)

            self.processor.clean_data(config['cleaning_operations'])
            self.processor.save_data(**config['output'])

            self.assertTrue(os.path.exists(config['output']['file_path']))

        asyncio.run(run_test())

    # Add more tests for other processor methods and scenarios

if __name__ == '__main__':
    unittest.main()