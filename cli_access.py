from argparse import ArgumentParser
from FilMoreBlanks.blanket_fill import BlanketFill
import yaml
from os import path, makedirs, replace
import pandas as pd

TOP_DIR = path.dirname(path.abspath(__file__))


def access_fill():
    parser = ArgumentParser(prog='FilMoreBlanks CSV filler')
    mandatory_args = parser.add_argument_group(title='FilMoreBlanks Mandatory Fields')
    mandatory_args.add_argument('-config_file', help='YAML config file for FilMoreBlanks', required=True, type=str)

    args = parser.parse_args()

    config_file = create_file_path(folder='FilMoreBlanks_Configs', file_name=args.config_file)
    with open(config_file, "r") as stream:
        config_file = yaml.safe_load(stream)

    # get CSV file
    csv_loc = config_file['CSV_filename']
    csv_data = pd.read_csv(csv_loc)
    # init FilMo
    blank_it = BlanketFill(csv_data)

    # generate new CSV
    blank_it.fix_csv(config_dict=config_file['change_list'], affect_only_columns_dict=config_file.get('affect_only_columns'))

    # move file to archive and save new CSV.
    create_file_path('archived', config_file['CSV_filename'])
    save_csv_data(blank_it.filled_data, f"COMPLETED_{config_file['CSV_filename']}")


def save_csv_data(data: pd.DataFrame, save_name):
    fname = create_file_path('filled_files', file_name=save_name)
    data.to_csv(fname, index=False)


def create_file_path(folder: str, file_name: str):
    allowed_exts = ['csv', 'yaml']

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


if __name__ == "__main__":
    access_fill()
