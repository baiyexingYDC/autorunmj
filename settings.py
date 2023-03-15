import argparse
import os

import yaml

def load_config():
    # Create a parser object
    parser = argparse.ArgumentParser()

    # Add an argument for environment name
    parser.add_argument('--env', default='dev', help='environment name')

    # Parse the command line arguments
    args = parser.parse_args()

    # Load the yaml file
    with open('config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # Get the config for the current environment
    config = config[args.env]

    # Return the config object
    return config


def create_dir():
    resize_path = "resize"
    temp_path = "temp"
    error_screenshot_path = "error_screenshot"
    log_path = "log"
    if not os.path.exists(resize_path):
        os.makedirs(resize_path)
    if not os.path.exists(error_screenshot_path):
        os.makedirs(error_screenshot_path)
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
