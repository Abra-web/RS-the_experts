from storage_handler import Storage,join, DIR_DATA_CSV, DIR_DATA_JSON
import glob
from file_processor import process_all


if __name__ == '__main__':
    storage= Storage()
    process_all(storage)