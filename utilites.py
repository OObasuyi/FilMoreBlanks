from os import path, makedirs, replace

import pandas as pd

TOP_DIR = path.dirname(path.abspath(__file__))


def create_file_path(folder: str, file_name: str):

    allowed_exts = ['csv','yaml']

    input_ext = '.'.join(file_name.split(".")[1:])
    if input_ext.lower() not in allowed_exts:
        raise ValueError(f'please ensure you using one of the allowed file types you gave {input_ext}')

    fName = f'{TOP_DIR}/{folder}/{file_name}'
    if not path.exists(f'{TOP_DIR}/{folder}'):
        makedirs(f'{TOP_DIR}/{folder}')

    # move file to correct dir if needed
    if not path.exists(fName):
        try:
            replace(f'{TOP_DIR}/{file_name}', fName)
        except:
            # file has yet to be created or not in top path
            pass
    return fName


def get_yaml_file(file_name):
    import yaml
    with open(file_name, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as yaml_error:
            return TypeError(yaml_error)


def save_csv_data(data:pd.DataFrame,save_name):
    fname = create_file_path('filled_files', file_name=save_name)
    data.to_csv(fname,index=False)


def move_spent_csv(file_name):
    old_storage_path = path.join(TOP_DIR,'digest', file_name)
    fname = create_file_path('archived',file_name)
    new_storage_path = path.join(TOP_DIR,'archived', fname)
    replace(old_storage_path, new_storage_path)
