from storage_handler import Storage, DIR_DATA_CSV, DIR_DATA_JSON
import glob



if __name__ == '__main__':
    storage = Storage()
    json_files=glob.glob(DIR_DATA_JSON+"*.json")
    print(json_files[0])
