import pandas as pd
import numpy as np
import cv2
import re
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self, data):
        self.data = data

    def remove_duplicates(self, subset=None):
        if isinstance(self.data, pd.DataFrame):
            self.data.drop_duplicates(subset=subset, inplace=True)

    def handle_missing_values(self, strategy='mean', columns=None):
        if isinstance(self.data, pd.DataFrame):
            if columns is None:
                columns = self.data.columns
            for col in columns:
                if strategy == 'mean':
                    self.data[col].fillna(self.data[col].mean(), inplace=True)
                elif strategy == 'median':
                    self.data[col].fillna(self.data[col].median(), inplace=True)
                elif strategy == 'mode':
                    self.data[col].fillna(self.data[col].mode().iloc[0], inplace=True)
                elif strategy == 'forward':
                    self.data[col].fillna(method='ffill', inplace=True)
                elif strategy == 'backward':
                    self.data[col].fillna(method='bfill', inplace=True)
                elif strategy == 'interpolate':
                    self.data[col].interpolate(inplace=True)
                elif strategy == 'drop':
                    self.data.dropna(subset=[col], inplace=True)

    def normalize_column_names(self):
        if isinstance(self.data, pd.DataFrame):
            self.data.columns = self.data.columns.str.lower().str.replace(' ', '_')

    def convert_data_types(self, type_dict):
        if isinstance(self.data, pd.DataFrame):
            for col, dtype in type_dict.items():
                try:
                    self.data[col] = self.data[col].astype(dtype)
                except Exception as e:
                    logger.warning(f"{col} 컬럼을 {dtype} 타입으로 변환 중 오류 발생: {str(e)}")

    def remove_outliers(self, columns, method='zscore', threshold=3):
        if isinstance(self.data, pd.DataFrame):
            for col in columns:
                if method == 'zscore':
                    z_scores = np.abs((self.data[col] - self.data[col].mean()) / self.data[col].std())
                    self.data = self.data[z_scores < threshold]
                elif method == 'iqr':
                    Q1 = self.data[col].quantile(0.25)
                    Q3 = self.data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    self.data = self.data[~((self.data[col] < (Q1 - 1.5 * IQR)) | (self.data[col] > (Q3 + 1.5 * IQR)))]

    def normalize_data(self, columns, method='minmax'):
        if isinstance(self.data, pd.DataFrame):
            for col in columns:
                if method == 'minmax':
                    self.data[col] = (self.data[col] - self.data[col].min()) / (self.data[col].max() - self.data[col].min())
                elif method == 'zscore':
                    self.data[col] = (self.data[col] - self.data[col].mean()) / self.data[col].std()

    def handle_categorical_data(self, columns, method='onehot'):
        if isinstance(self.data, pd.DataFrame):
            for col in columns:
                if method == 'onehot':
                    self.data = pd.get_dummies(self.data, columns=[col])
                elif method == 'label':
                    self.data[col] = pd.Categorical(self.data[col]).codes

    def clean_text_data(self, columns):
        if isinstance(self.data, pd.DataFrame):
            for col in columns:
                self.data[col] = self.data[col].apply(lambda x: re.sub(r'[^\w\s]', '', str(x).lower()))

    def format_dates(self, columns, date_format='%Y-%m-%d'):
        if isinstance(self.data, pd.DataFrame):
            for col in columns:
                self.data[col] = pd.to_datetime(self.data[col], format=date_format)

    def resize_image(self, size):
        if isinstance(self.data, np.ndarray) and len(self.data.shape) == 3:
            self.data = cv2.resize(self.data, size)

    def convert_color_space(self, conversion):
        if isinstance(self.data, np.ndarray) and len(self.data.shape) == 3:
            self.data = cv2.cvtColor(self.data, conversion)

    def apply_filter(self, filter_type, **kwargs):
        if isinstance(self.data, np.ndarray) and len(self.data.shape) == 3:
            if filter_type == 'blur':
                self.data = cv2.blur(self.data, **kwargs)
            elif filter_type == 'gaussian':
                self.data = cv2.GaussianBlur(self.data, **kwargs)
            elif filter_type == 'median':
                self.data = cv2.medianBlur(self.data, **kwargs)

    def process_frames(self, operation, **kwargs):
        if isinstance(self.data, list) and all(isinstance(frame, np.ndarray) for frame in self.data):
            for i, frame in enumerate(self.data):
                if operation == 'resize':
                    self.data[i] = cv2.resize(frame, **kwargs)
                elif operation == 'convert_color':
                    self.data[i] = cv2.cvtColor(frame, **kwargs)
                elif operation == 'filter':
                    if kwargs['filter_type'] == 'blur':
                        self.data[i] = cv2.blur(frame, **kwargs['ksize'])
                    elif kwargs['filter_type'] == 'gaussian':
                        self.data[i] = cv2.GaussianBlur(frame, **kwargs['ksize'], **kwargs['sigmaX'])
                    elif kwargs['filter_type'] == 'median':
                        self.data[i] = cv2.medianBlur(frame, **kwargs['ksize'])