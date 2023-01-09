import pandas as pd
from .utilites import create_file_path


class BlanketFill:
    def __init__(self, csv_name):
        """ CSV must have features/col headers"""
        self.csv_loc = create_file_path('digest', csv_name)
        self.csv_data = pd.read_csv(self.csv_loc)

    def populate_csv(self, attr_to_change: tuple, selected_cols: list = 'all'):
        ''' old change such occupy first pos, new change second pos'''
        if len(attr_to_change) != 2:
            raise ValueError(f'attr_to_change value should only contain TWO values. We received {len(attr_to_change)}')

        old_val, new_val = attr_to_change[0], attr_to_change[1]
        new_val = new_val if isinstance(new_val, list) else [new_val]

        if not isinstance(selected_cols, list):
            if selected_cols == 'all':
                selected_cols = self.csv_data.columns.tolist()
            else:
                selected_cols = [selected_cols]

        new_data_collect = []
        gather_old_idx = []
        for idx in self.csv_data.index:
            row_data = self.csv_data.loc[idx]
            for col in selected_cols:
                col_data = row_data[col]
                if isinstance(col_data, float):
                    try:
                        col_data = str(int(col_data)).lstrip().rstrip()
                    except:
                        continue
                else:
                    col_data = str(col_data).lstrip().rstrip()

                if old_val != col_data:
                    continue
                else:
                    gather_old_idx.append(idx)
                    old_row = row_data.to_dict()
                    for nv in new_val:
                        new_row = old_row.copy()
                        new_row[col] = nv
                        new_data_collect.append(new_row)

        self.csv_data.drop(gather_old_idx, inplace=True)
        self.csv_data.reset_index(inplace=True, drop=True)
        new_data = pd.DataFrame(new_data_collect)
        self.csv_data = pd.concat([self.csv_data, new_data], ignore_index=True)
        self.csv_data.drop_duplicates(inplace=True)

