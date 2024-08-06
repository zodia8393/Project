import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlalchemy import create_engine
import json
import xml.etree.ElementTree as ET
import cv2
import aiohttp
import asyncio
import os
import logging
import tempfile
import zipfile
import tarfile

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        self.data = None

    async def collect_from_web(self, url, parser='html.parser', target_elements=None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, parser)
                    if target_elements:
                        data = soup.find_all(**target_elements)
                    else:
                        data = soup.find_all()
                    self.data = pd.DataFrame([elem.text for elem in data])
        except Exception as e:
            logger.error(f"웹에서 데이터 수집 중 오류 발생: {str(e)}")
            raise

    async def collect_from_api(self, api_url, params=None, headers=None, method='GET'):
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(api_url, params=params, headers=headers) as response:
                        json_data = await response.json()
                elif method == 'POST':
                    async with session.post(api_url, json=params, headers=headers) as response:
                        json_data = await response.json()
                self.data = pd.DataFrame(json_data)
        except Exception as e:
            logger.error(f"API에서 데이터 수집 중 오류 발생: {str(e)}")
            raise

    def collect_from_db(self, db_path, query, db_type='sqlite'):
        try:
            if db_type == 'sqlite':
                conn = sqlite3.connect(db_path)
            else:
                engine = create_engine(db_path)
                conn = engine.connect()
            self.data = pd.read_sql_query(query, conn)
            conn.close()
        except Exception as e:
            logger.error(f"데이터베이스에서 데이터 수집 중 오류 발생: {str(e)}")
            raise

    def collect_from_file(self, file_path, file_type, **kwargs):
        try:
            if file_type == 'csv':
                self.data = pd.read_csv(file_path, **kwargs)
            elif file_type == 'json':
                with open(file_path, 'r') as f:
                    self.data = pd.DataFrame(json.load(f))
            elif file_type == 'xml':
                tree = ET.parse(file_path)
                root = tree.getroot()
                data = []
                for child in root:
                    data.append({elem.tag: elem.text for elem in child})
                self.data = pd.DataFrame(data)
            elif file_type in ['xls', 'xlsx']:
                self.data = pd.read_excel(file_path, **kwargs)
            elif file_type == 'parquet':
                self.data = pd.read_parquet(file_path, **kwargs)
            elif file_type == 'hdf':
                self.data = pd.read_hdf(file_path, **kwargs)
            elif file_type == 'feather':
                self.data = pd.read_feather(file_path, **kwargs)
            else:
                raise ValueError(f"지원하지 않는 파일 타입: {file_type}")
        except Exception as e:
            logger.error(f"{file_type} 파일에서 데이터 수집 중 오류 발생: {str(e)}")
            raise

    def collect_from_image(self, file_path):
        try:
            self.data = cv2.imread(file_path)
            if self.data is None:
                raise ValueError("이미지를 읽을 수 없습니다.")
        except Exception as e:
            logger.error(f"이미지 파일에서 데이터 수집 중 오류 발생: {str(e)}")
            raise

    def collect_from_video(self, file_path):
        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                raise ValueError("비디오를 열 수 없습니다.")
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            cap.release()
            self.data = frames
        except Exception as e:
            logger.error(f"비디오 파일에서 데이터 수집 중 오류 발생: {str(e)}")
            raise

    def collect_from_directory(self, dir_path, file_type):
        try:
            all_data = []
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(file_type):
                        file_path = os.path.join(root, file)
                        self.collect_from_file(file_path, file_type)
                        all_data.append(self.data)
            self.data = pd.concat(all_data, ignore_index=True)
        except Exception as e:
            logger.error(f"디렉토리에서 데이터 수집 중 오류 발생: {str(e)}")
            raise

    def collect_from_archive(self, archive_path, archive_type, file_type):
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                if archive_type == 'zip':
                    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                elif archive_type in ['tar', 'gz', 'bz2']:
                    with tarfile.open(archive_path, 'r:*') as tar_ref:
                        tar_ref.extractall(temp_dir)
                else:
                    raise ValueError(f"지원하지 않는 아카이브 타입: {archive_type}")
                
                self.collect_from_directory(temp_dir, file_type)
        except Exception as e:
            logger.error(f"아카이브에서 데이터 수집 중 오류 발생: {str(e)}")
            raise