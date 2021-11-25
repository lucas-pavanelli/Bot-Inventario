import unittest
import os
import shutil
import json
import update_xlsx


class TestUpdate(unittest.TestCase):
    def setUp(self):
        shutil.copy("./test_files/31_05_2021_TEST_FILE.xlsx",
                    "./Staging/31_05_2021_TEST_FILE.xlsx")

    def tearDown(self):
        update_xlsx.clean_staging_area(
            "31_05_2021_TEST_FILE.xlsx", folder="./Staging/")

    def test_update(self):
        file_name, date = update_xlsx.get_date()
        self.assertEqual(file_name, "31_05_2021_TEST_FILE.xlsx")
        self.assertEqual(update_xlsx.write_date(date, "./test_files/last_update_TEST_FILE.json"),
                         "Last Update date is now: Day 31, Month 5, Year 2021")

        self.assertEqual(update_xlsx.write_input_file("31_05_2021_TEST_FILE.xlsx",
                                                      destination="./test_files/31_05_2021_TEST_FILE.xlsx"), "Success, Input File Updated")


if __name__ == "__main__":
    unittest.main()
