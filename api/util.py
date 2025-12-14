import yaml
import joblib
import platform
import os
from pathlib import Path

# Adjusting paths for the new structure where everything is relative to the app execution directory

def get_dir():
    return Path(os.getcwd())

def load_params(lokasi_file):
    with open(lokasi_file, 'r') as file:
        params = yaml.safe_load(file)
    return params

def pickle_load(file_path: str):
    return joblib.load(file_path)

def pickle_dump(data, file_path: str) -> None:
    joblib.dump(data, file_path)

# Simplified path helpers
def get_config_path():
    # Assuming config is in ./config relative to where we run the script
    return os.path.join(os.getcwd(), "config", "params.yaml")

def get_model_path(config):
    # Model path from config might be 'models/production_model.pkl'
    # Check if it exists relative to config, or just use it as relative to cwd
    model_rel_path = config["production_model_path"]
    return os.path.join(os.getcwd(), model_rel_path)