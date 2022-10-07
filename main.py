from storage_handler import Storage, join, DIR_DATA_CSV, DIR_DATA_JSON, Type
import glob
from file_processor import process_all


if __name__ == '__main__':
    storage= Storage()
    #process_all(storage)
    #storage.extract(100)
    #storage.sort(Type.EXTRACT,'pid')
    #storage.sort(Type.EXTRACT,'track_uri')
    storage.make_songs(Type.EXTRACT)