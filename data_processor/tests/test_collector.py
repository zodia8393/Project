import unittest
import asyncio
import pandas as pd
import numpy as np
import os
import tempfile
import json
import cv2
from src.collector import DataCollector

class TestDataCollector(unittest.TestCase):
    def setUp(self):
        self.collector = DataCollector()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_collect_from_file_csv(self):
        # Create a test CSV file
        test_df = pd.DataFrame({'A': [1, 2, 3], 'B': ['a', 'b', 'c']})
        test_file = os.path.join(self.temp_dir, 'test.csv')
        test_df.to_csv(test_file, index=False)

        self.collector.collect_from_file(test_file, 'csv')
        self.assertIsNotNone(self.collector.data)
        self.assertEqual(len(self.collector.data), 3)
        self.assertListEqual(list(self.collector.data.columns), ['A', 'B'])

    def test_collect_from_file_json(self):
        # Create a test JSON file
        test_data = [{'A': 1, 'B': 'a'}, {'A': 2, 'B': 'b'}, {'A': 3, 'B': 'c'}]
        test_file = os.path.join(self.temp_dir, 'test.json')
        with open(test_file, 'w') as f:
            json.dump(test_data, f)

        self.collector.collect_from_file(test_file, 'json')
        self.assertIsNotNone(self.collector.data)
        self.assertEqual(len(self.collector.data), 3)
        self.assertListEqual(list(self.collector.data.columns), ['A', 'B'])

    @unittest.skip("Requires internet connection")
    def test_collect_from_web(self):
        async def run_test():
            await self.collector.collect_from_web('https://example.com')
            self.assertIsNotNone(self.collector.data)
            self.assertTrue(len(self.collector.data) > 0)

        asyncio.run(run_test())

    @unittest.skip("Requires API setup")
    def test_collect_from_api(self):
        async def run_test():
            await self.collector.collect_from_api('https://api.example.com/data')
            self.assertIsNotNone(self.collector.data)
            self.assertTrue(len(self.collector.data) > 0)

        asyncio.run(run_test())

    def test_collect_from_image(self):
        # Create a test image
        test_image = np.random.rand(100, 100, 3) * 255
        test_image = test_image.astype(np.uint8)
        test_file = os.path.join(self.temp_dir, 'test_image.jpg')
        cv2.imwrite(test_file, test_image)

        self.collector.collect_from_image(test_file)
        self.assertIsNotNone(self.collector.data)
        self.assertEqual(self.collector.data.shape, (100, 100, 3))

    def test_collect_from_video(self):
        # Create a test video
        test_video = [np.random.rand(100, 100, 3) * 255 for _ in range(10)]
        test_video = [frame.astype(np.uint8) for frame in test_video]
        test_file = os.path.join(self.temp_dir, 'test_video.mp4')
        out = cv2.VideoWriter(test_file, cv2.VideoWriter_fourcc(*'mp4v'), 30, (100, 100))
        for frame in test_video:
            out.write(frame)
        out.release()

        self.collector.collect_from_video(test_file)
        self.assertIsNotNone(self.collector.data)
        self.assertEqual(len(self.collector.data), 10)
        self.assertEqual(self.collector.data[0].shape, (100, 100, 3))

    def test_collect_from_directory(self):
        # Create test CSV files in the directory
        for i in range(3):
            test_df = pd.DataFrame({'A': [i, i+1, i+2], 'B': ['a', 'b', 'c']})
            test_file = os.path.join(self.temp_dir, f'test_{i}.csv')
            test_df.to_csv(test_file, index=False)

        self.collector.collect_from_directory(self.temp_dir, 'csv')
        self.assertIsNotNone(self.collector.data)
        self.assertEqual(len(self.collector.data), 9)
        self.assertListEqual(list(self.collector.data.columns), ['A', 'B'])

if __name__ == '__main__':
    unittest.main()