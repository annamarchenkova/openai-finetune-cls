import os
import yaml

# import pkgutil
from utils_project_dirs import PROJECT_DIR

def load_config(cnf_dir=PROJECT_DIR, cnf_name="config.yml"):
    """
    load the yaml file
    """
    config_file = open(os.path.join(cnf_dir, cnf_name))
    return yaml.load(config_file, yaml.FullLoader)
