from argparse import ArgumentParser
import FilMoreBlanks.utilites as utilites
from FilMoreBlanks.blanket_fill import BlanketFill


def access_fil():
    parser = ArgumentParser(prog='FilMoreBlanks CSV filler')
    mandatory_args = parser.add_argument_group(title='FilMoreBlanks Mandatory Fields')
    mandatory_args.add_argument('-config_file', help='YAML config file for FilMoreBlanks', required=True, type=str)

    args = parser.parse_args()

    config_file = utilites.create_file_path(folder='FilMoreBlanks_Configs', file_name=args.config_file)
    config_file = utilites.get_yaml_file(config_file)

    # get CSV file
    blank_it = BlanketFill(config_file['CSV_filename'])
    # since it stored a dict, include the key as a tuple item as an argument.
    for k,v in config_file['change_list'].items():
        # type check
        if not isinstance(v,list):
            raise ValueError(f'THE RECEIVED VALUE IS NOT A LIST ITEM. you supplied a {type(v)}')

        change_item = tuple([k,v])
        # if BOTH keys match then we must only want to work on specific column(s)
        for k_affect,only_affect in config_file['affect_only_columns'].items():
            if k_affect == k:
                only_affect = only_affect if isinstance(only_affect,list) else [only_affect]
                blank_it.populate_csv(attr_to_change=change_item,selected_cols=only_affect)
            else:
                blank_it.populate_csv(attr_to_change=change_item)
    # move file to spent and return new CSV.
    utilites.move_spent_csv(config_file['CSV_filename'])
    utilites.save_csv_data(blank_it.csv_data,f"COMPLETED_{config_file['CSV_filename']}")


if __name__ == "__main__":
    access_fil()
