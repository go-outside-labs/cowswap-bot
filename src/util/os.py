# -*- encoding: utf-8 -*-
# utils/os.py
# This class implements OS/file system util methods used by the other classes.

import os
import sys
import json
import copy
import logging
from pathlib import Path
from dotenv import load_dotenv


def set_logging(log_level) -> None:
    """Set logging level according to .env config."""

    if log_level == 'info':
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    elif log_level == 'error':
        logging.basicConfig(level=logging.ERROR, format='%(message)s')

    elif log_level == 'debug':
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    else:
        print(f'Logging level {log_level} is not available.')



def load_config() -> dict:
    """Load and set environment variables."""

    env_file = Path('.') / '.env'
    if not os.path.isfile(env_file):
        log_error(f'Please create an .env file')
        sys.exit(1)

    env_vars = {}
    load_dotenv(env_file)

    try:
        env_vars['OUTPUT_DIR'] = os.getenv("OUTPUT_DIR")
        env_vars['OUTPUT_FILE_STR'] = os.getenv("OUTPUT_FILE_STR")
        env_vars['INPUT_FILE_STR'] = os.getenv("INPUT_FILE_STR") 

        set_logging(os.getenv("LOG_LEVEL"))

        return env_vars

    except KeyError as e:
        log_error(f'Cannot extract env variables: {e}. Exiting.')
        raise


def log_error(string) -> None:
    """Print STDOUT error using the logging library."""
    logging.error(f'🚨 {string}')


def log_info(string) -> None:
    """Print STDOUT info using the logging library."""
    logging.info(f'✅ {string}')


def log_debug(string) -> None:
    """Print STDOUT debug using the logging library."""
    logging.debug(f'🟨 {string}')


def open_json(filepath) -> dict:
    """Load and parse a file."""

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    except (IOError, FileNotFoundError) as e:
        log_error(f'Failed to parse: "{filepath}": {e}')
        sys.exit(1)


def format_path(dir_path, filename) -> str:
    """Format a OS full filepath."""
    return os.path.join(dir_path, filename)


def format_output_file(name) -> str:
    """Format the name for the result file."""
    return f'{name}.json'


def save_output(destination, data) -> None:
    """Save data from memory to a destination in disk."""

    try:
        with open(destination, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    except IOError as e:
        log_error(f'Could not save {destination}: {e}')


def create_dir(result_dir) -> None:
    """Check whether a directory exists and create it if needed."""
    try:
        if not os.path.isdir(result_dir):
            os.mkdir(result_dir)
            
    except OSError as e:
        log_error(f'Could not create {result_dir}: {e}')


def set_output(env_vars, input_file) -> str:
    """Create an output destination to save solutions."""

    try:
        output_dir = env_vars['OUTPUT_DIR']
        create_dir(output_dir)

        output_str = input_file.split('_')[1].split('.json')[0] 
        output_file_str = env_vars['OUTPUT_FILE_STR']
        output_file = output_file_str.format(output_str)
        return format_path(output_dir, output_file)

    except (TypeError, KeyError) as e:
        log_error(f'Could not format output file. Check .env')
        sys.exit(1)

def deep_copy(dict_to_clone) -> dict:
    """Deep copy (not reference copy) to a dict."""
    return copy.deepcopy(dict_to_clone)
