import sys
from src.constants import INGESTION_STAGE_NAME
from src.components.data_ingestion import IngestData
from src.logger import logging
from src.exception import MyException

class DataIngestionPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        upload = IngestData()
        upload.download_file()
        upload.extract_zip_file()

if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} started <<<<<<")
        obj = DataIngestionPipeline()
        obj.main()
    except MyException as e:
            raise MyException(e, sys)