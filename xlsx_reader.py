import pandas as pd
import json


class XlsxReader():
    def __init__(self, file_path='./data/input_file.xlsx'):
        self.xlsx = pd.ExcelFile(file_path)

    def get_main_sheet(self, sheet_name, col_list=[]):
        self.columns = col_list
        self.sheet = pd.read_excel(self.xlsx, sheet_name)
        self.sheet = XlsxReader.select_cols(self)
        return self.sheet

    def select_cols(self):
        # clean
        # PK should not be null
        self.sheet = self.sheet[self.sheet[self.columns[0]].notna()]
        # typo in column naming + selecting cols
        try:
            self.sheet = self.sheet[self.columns]
        except:
            try:
                self.columns[-1] = 'Avaiable'
                self.sheet = self.sheet[self.columns]
            except:
                raise KeyError(
                    'Please check if the column names in the excel file/sheet are: {}'.format(self.columns))
        return self.sheet.fillna(0)

    def drop_equals(self, fast_track=False):
        """ADD LAST 5 COLS GIVEN THAT THE CISCO STANDARD PART NUMBER MATCH"""
        # clean duplicates, but method is tightly coupled... REVIEW LATER
        if fast_track:
            aux_df = self.sheet.groupby([self.columns[0]])[
                self.columns[1:]].transform('sum')
            preamble_df = self.sheet[self.columns[:1]]
            self.sheet = pd.concat([preamble_df, aux_df], axis=1)
            self.sheet = self.sheet.drop_duplicates(subset=[self.columns[0]])

        else:
            aux_df = self.sheet.groupby([self.columns[0]])[
                self.columns[3:]].transform('sum')
            preamble_df = self.sheet[self.columns[:3]]
            self.sheet = pd.concat([preamble_df, aux_df], axis=1)
            self.sheet = self.sheet.drop_duplicates(subset=[self.columns[0]])
        return self.sheet.reset_index(drop=True)


# package data into dict of dfs

def json_dict(sheet_names, col_list, dict=dict(), file_path='./data/input_file.xlsx', fast_track=False):
    for sheet in sheet_names:
        data = XlsxReader(file_path=file_path)
        df = data.get_main_sheet(sheet_name=sheet, col_list=col_list)
        df = data.drop_equals(fast_track)
        dict[sheet] = df.to_json(orient='index')
    return json.dumps(dict, indent=4)
# package into json format to transfer data


def df_dict(sheet_names, col_list, file_path='./data/input_file.xlsx', fast_track=False):
    dict_=dict()
    for sheet in sheet_names:
        data = XlsxReader(file_path=file_path)
        df = data.get_main_sheet(sheet_name=sheet, col_list=col_list)
        df = data.drop_equals(fast_track)
        dict_[sheet] = df
    return dict_

# reverse the process done in df_to_json


def json_to_df(dict=dict()):
    dict = json.loads(dict)
    for key in dict.keys():
        #dict = json.loads(dict)
        dict[key] = pd.read_json(dict[key], orient='index')
    return dict
