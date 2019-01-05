import unittest
import json
from custom_code.tools.thinkstats import get_trimmed_and_cleaned_dataframe


class DataIntegrityTestSuite(unittest.TestCase):
    def read_validation_data(self):
        with open(
            "/Users/meilfort/Code/metis/ThinkStats2/custom_code/data/2002FemPregCodeBookSummary.json",
            "r",
        ) as json_file:
            validation_data = json.load(json_file)
            return validation_data

    def setUp(self):
        self.validation_data = self.read_validation_data()
        self.df = get_trimmed_and_cleaned_dataframe(data_path="custom_code/data")
        # pass

    def tearDown(self):
        pass

    def assertAllValues(
        self, variable_name, key_func=lambda column, value: column == int(value)
    ):
        variable_data = self.validation_data[variable_name]
        values = variable_data["values"].keys()
        for value in values:
            self.assertEqual(
                variable_data["values"][value],
                len(self.df[key_func(self.df[variable_name], value)]),
                f"The {variable_name} values for the {variable_data['labels'][value]} do not match.",
            )

    def test_caseid_total_count(self):
        self.assertEqual(
            self.validation_data["caseid"]["total"],
            len(self.df.caseid),
            f"The total count of caseids should equal the total value from the validation_data.",
        )

    def test_pregordr_counts(self):
        self.assertAllValues("pregordr")

    def test_prglngth_counts(self):
        prglngth = self.validation_data["prglngth"]

        self.assertEqual(
            prglngth["values"]["1"],
            len(self.df[self.df["prglngth"] <= 13]),
            f"The preglenth values for the pregnancy length of {prglngth['labels']['1']} do not match.",
        )

        self.assertEqual(
            prglngth["values"]["2"],
            len(self.df[(self.df["prglngth"] >= 14) & (self.df["prglngth"] <= 26)]),
            f"The preglenth values for the pregnancy length of {prglngth['labels']['2']} do not match.",
        )

        self.assertEqual(
            prglngth["values"]["3"],
            len(self.df[self.df["prglngth"] >= 27]),
            f"The preglenth values for the pregnancy length of {prglngth['labels']['3']} do not match.",
        )

    def test_outcome_counts(self):
        self.assertAllValues("outcome")

    def test_birthord_count(self):
        self.assertAllValues(
            "birthord",
            key_func=lambda column, value: column.isnull()
            if int(value) == 0
            else column == int(value),
        )

    def test_birthwgt_lb_nan_count(self):
        birthwgt_lb = self.validation_data["birthwgt_lb"]
        nan_sum = (
            birthwgt_lb["values"]["0"]
            + birthwgt_lb["values"]["97"]
            + birthwgt_lb["values"]["98"]
            + birthwgt_lb["values"]["99"]
        )
        self.assertEqual(
            len(self.df[self.df["birthwgt_lb"].isnull()]),
            nan_sum,
            f"The birthwgt_lb nan values do not match.",
        )

    def test_birthwgt_lb_no_value_over_world_record(self):
        max_weight = 22
        self.assertLess(
            self.df.birthwgt_lb.max(),
            max_weight,
            "The max value for the birthwgt_lb column is larger than the max_weight ever recorded. Check the values!",
        )

    def test_agepreg_nan_count(self):
        agepreg = self.validation_data["agepreg"]
        self.assertEqual(
            len(self.df[self.df["agepreg"].isnull()]),
            agepreg["values"]["0"],
            f"The agepreg nan values do not match.",
        )
