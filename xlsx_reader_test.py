import unittest
import json
import xlsx_reader
import pandas_queries
import pandas as pd


class TestXlsxReader(unittest.TestCase):
    def test_df_to_json(self):
        # setup
        main_name_list = ['Ingram', 'Scansource', 'Comstor']
        col_list = ['Cisco Standard Part Number', 'Distributor Part Number', 'Product Item Description', 'Quantity on Hand', 'Quantity On Order',
                    'Distributor Reported In-transit Quantity', 'Committed Quantity', 'Available']

        # Loads previously saved json file
        with open("./test_files/serialized_df_TEST_FILE.json", "r") as json_file:
            verified_df = json.load(json_file)
        df_dict = xlsx_reader.json_dict(
            sheet_names=main_name_list, col_list=col_list, file_path="./test_files/31_05_2021_TEST_FILE.xlsx")

        # testa
        self.assertEqual(df_dict, verified_df)

    def test_json_to_df(self):

        # setup
        main_name_list = ['Ingram', 'Scansource', 'Comstor']
        col_list = ['Cisco Standard Part Number', 'Distributor Part Number', 'Product Item Description', 'Quantity on Hand', 'Quantity On Order',
                    'Distributor Reported In-transit Quantity', 'Committed Quantity', 'Available']
        df_dict = xlsx_reader.json_dict(
            sheet_names=main_name_list, col_list=col_list, file_path="./test_files/31_05_2021_TEST_FILE.xlsx")
        df_dict = xlsx_reader.json_to_df(dict=df_dict)

        # Conditions
        self.assertEqual(
            str(type(df_dict["Ingram"])), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df_dict["Ingram"].size, 1872)
        self.assertEqual(
            str(type(df_dict["Scansource"])), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df_dict["Scansource"].size, 2896)
        self.assertEqual(
            str(type(df_dict["Comstor"])), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df_dict["Comstor"].size, 3936)

    def test_get_main_sheet(self):
        data = xlsx_reader.XlsxReader(
            file_path="./test_files/31_05_2021_TEST_FILE.xlsx")
        col_list = ['Cisco Standard Part Number', 'Distributor Part Number', 'Product Item Description', 'Quantity on Hand', 'Quantity On Order',
                    'Distributor Reported In-transit Quantity', 'Committed Quantity', 'Available']
        df = data.get_main_sheet(sheet_name='Ingram', col_list=col_list)
        df = data.drop_equals()
        self.assertEqual(df.size, 1872)

    def test_df_dict(self):
        # setup
        main_name_list = ['Ingram', 'Scansource', 'Comstor']
        col_list = ['Cisco Standard Part Number', 'Distributor Part Number', 'Product Item Description', 'Quantity on Hand', 'Quantity On Order',
                    'Distributor Reported In-transit Quantity', 'Committed Quantity', 'Available']
        df_dict = xlsx_reader.df_dict(
            sheet_names=main_name_list, col_list=col_list, file_path="./test_files/31_05_2021_TEST_FILE.xlsx")

        self.assertEqual(
            str(type(df_dict["Ingram"])), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df_dict["Ingram"].size, 1872)
        self.assertEqual(
            str(type(df_dict["Scansource"])), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df_dict["Scansource"].size, 2896)
        self.assertEqual(
            str(type(df_dict["Comstor"])), "<class 'pandas.core.frame.DataFrame'>")
        self.assertEqual(df_dict["Comstor"].size, 3936)

    def test_product_query(self):
        main_name_list = ['Ingram', 'Scansource', 'Comstor']
        col_list = ['Cisco Standard Part Number', 'Distributor Part Number', 'Product Item Description', 'Quantity on Hand', 'Quantity On Order',
                    'Distributor Reported In-transit Quantity', 'Committed Quantity', 'Available']
        df_dict = xlsx_reader.df_dict(
            sheet_names=main_name_list, col_list=col_list, file_path="./test_files/31_05_2021_TEST_FILE.xlsx")
        ingram_test = pandas_queries.product_query(
            df_dict["Ingram"], "WS-C2960X-24PS-BR", 'Cisco Standard Part Number')
        comstor_test = pandas_queries.product_query(
            df_dict["Comstor"], "5-CBW240AC-B", 'Cisco Standard Part Number')
        scansource_test = pandas_queries.product_query(
            df_dict["Scansource"], "FPR1120-NGFW-K9", 'Cisco Standard Part Number')

        self.assertEqual(ingram_test, {'WS-C2960X-24PS-BR': 1})
        self.assertEqual(comstor_test["5-CBW240AC-B"], "Not Available")
        self.assertEqual(scansource_test["FPR1120-NGFW-K9"], 2)

    def test_reading_FT(self):

        sheet_names = ["Ingram Fast Track",
                       "Comstor Fast Track", "Scansource Fast Track"]
        col_list = ["FT Part Number", "Avaiable"]
        data = xlsx_reader.XlsxReader(
            file_path="./test_files/31_05_2021_TEST_FILE.xlsx")
        df_FT = data.get_main_sheet(
            sheet_name=sheet_names[0], col_list=col_list)
        df_FT = data.drop_equals(fast_track=True)

        self.assertEqual(df_FT.size, 210)
        ingram_ft_test = pandas_queries.product_query(
            df_FT, "CP-8841-K9=", 'FT Part Number')
        self.assertEqual(ingram_ft_test["CP-8841-K9="], 'Not Available')
        ingram_ft_test2 = pandas_queries.product_query(
            df_FT, "ASA5506-K9", 'FT Part Number')
        self.assertEqual(ingram_ft_test2["ASA5506-K9"], 1)
        ingram_ft_test3 = pd.read_json(pandas_queries.FT_TOP10(df_FT, col_list), orient='index')
        self.assertEqual(ingram_ft_test3.size, 20)
        self.assertEqual(ingram_ft_test3.iloc[0, 0],'GLC-SX-MMD=')


if __name__ == "__main__":
    unittest.main()
