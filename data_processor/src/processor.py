from .collector import DataCollector
from .cleaner import DataCleaner
from sqlalchemy import create_engine
import cv2
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.collector = DataCollector()
        self.cleaner = None

    async def collect_data(self, source_type, **kwargs):
        if source_type == 'web':
            await self.collector.collect_from_web(**kwargs)
        elif source_type == 'api':
            await self.collector.collect_from_api(**kwargs)
        elif source_type == 'db':
            self.collector.collect_from_db(**kwargs)
        elif source_type in ['csv', 'json', 'xml', 'xls', 'xlsx', 'parquet', 'hdf', 'feather']:
            self.collector.collect_from_file(file_type=source_type, **kwargs)
        elif source_type == 'image':
            self.collector.collect_from_image(**kwargs)
        elif source_type == 'video':
            self.collector.collect_from_video(**kwargs)
        elif source_type == 'directory':
            self.collector.collect_from_directory(**kwargs)
        elif source_type == 'archive':
            self.collector.collect_from_archive(**kwargs)
        else:
            raise ValueError(f"지원하지 않는 소스 타입: {source_type}")

        self.cleaner = DataCleaner(self.collector.data)

    def clean_data(self, operations):
        for op, params in operations.items():
            if hasattr(self.cleaner, op):
                getattr(self.cleaner, op)(**params)
            else:
                logger.warning(f"지원하지 않는 정제 작업: {op}")

    def save_data(self, output_type, **kwargs):
        if output_type == 'csv':
            self.cleaner.data.to_csv(**kwargs)
        elif output_type == 'json':
            self.cleaner.data.to_json(**kwargs)
        elif output_type == 'excel':
            self.cleaner.data.to_excel(**kwargs)
        elif output_type == 'parquet':
            self.cleaner.data.to_parquet(**kwargs)
        elif output_type == 'hdf':
            self.cleaner.data.to_hdf(**kwargs)
        elif output_type == 'feather':
            self.cleaner.data.to_feather(**kwargs)
        elif output_type == 'db':
            engine = create_engine(kwargs.pop('connection_string'))
            self.cleaner.data.to_sql(**kwargs, con=engine)
        elif output_type == 'image':
            cv2.imwrite(kwargs['file_path'], self.cleaner.data)
        elif output_type == 'video':
            out = cv2.VideoWriter(kwargs['file_path'], cv2.VideoWriter_fourcc(*'mp4v'), kwargs['fps'], kwargs['frame_size'])
            for frame in self.cleaner.data:
                out.write(frame)
            out.release()
        else:
            raise ValueError(f"지원하지 않는 출력 타입: {output_type}")