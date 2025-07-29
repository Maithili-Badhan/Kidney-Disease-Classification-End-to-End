import os
import zipfile
import gdown
import shutil
from src.cnnClassifier import logger
from src.cnnClassifier.utils.common import get_size
from src.cnnClassifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> str:
        '''
        Fetch data from the url
        '''
        try:
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_integration", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?export=download&id='
            gdown.download(prefix + file_id, zip_download_dir)

            logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")

        except Exception as e:
            raise e

    def extract_zip_file(self):
        """
        Extracts the zip file and moves Normal and Tumor folders into a specific directory
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        # ✅ Extract zip
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"Extracted zip file to: {unzip_path}")

        # ✅ Create a target folder to group the images
        output_dir = os.path.join(unzip_path, "kidney-ct-scan-image")
        os.makedirs(output_dir, exist_ok=True)

        # ✅ Move 'Normal' and 'Tumor' folders into the output directory
        for folder_name in ["Normal", "Tumor"]:
            src = os.path.join(unzip_path, folder_name)
            dst = os.path.join(output_dir, folder_name)
            if os.path.exists(src):
                shutil.move(src, dst)
                logger.info(f"Moved {folder_name} folder to {output_dir}")
            else:
                logger.warning(f"{folder_name} folder not found in extracted files.")