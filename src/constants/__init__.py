from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")

"""
---------------------------------------------------------------
Training Pipeline related constant start with DATA_INGESTION VAR NAME
---------------------------------------------------------------
"""
PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"
TRAINING_STAGE_NAME = "Training Pipeline"

"""
---------------------------------------------------------------
Environment Test and Dependency related constant 
---------------------------------------------------------------
"""
REQUIRED_PYTHON = "python3"
REQUIREMENTS_FILE = "requirements.txt"

"""
---------------------------------------------------------------
Data ingestion related constant 
---------------------------------------------------------------
"""
INGESTION_STAGE_NAME = "Data Ingestion"
"""
---------------------------------------------------------------
Data PrePrecessing related constant 
---------------------------------------------------------------
"""
PRE_PROCESSING_STAGE_NAME = "Data Pre-Processing"


"""
---------------------------------------------------------------
FEATURE Selection related constant 
---------------------------------------------------------------
"""
FEATURE_SELECTION_STAGE = "Feature Selection"

"""
---------------------------------------------------------------
Model Selection related constant 
---------------------------------------------------------------
"""
TRAIN_TEST_SPLIT_RATIO = 0.25