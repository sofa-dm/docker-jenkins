import unittest
import xmlrunner
import io
from checker_pymssql import DBChecker
from checker_pymssql import verify_allowed_values, verify_max_length, verify_completeness

out = io.BytesIO()
unittest.main(
    testRunner=xmlrunner.XMLTestRunner(output=out),
    failfast=False,
    buffer=False,
    catchbreak=False,
    exit=False)


class TestDatabase(unittest.TestCase):
    def test_dimgeography_check_table_is_not_empty(self):
        checker = DBChecker()
        output = checker.select_query(f"select count(*) from dbo.DimGeography;")
        is_passed = output[0][0] > 0
        print("test_dimgeography_check_table_is_not_empty:", is_passed)
        self.assertTrue(is_passed)

    def test_dimgeography_check_completeness_unique_countries_list(self):
        checker = DBChecker()
        output = checker.select_query(f"select distinct EnglishCountryRegionName from dbo.DimGeography")
        output_cleared = [i[0] for i in output]
        is_passed = verify_allowed_values(records=output_cleared,
                                          allowed_values=['Australia', 'Canada', 'France', 'Germany', 'United Kingdom',
                                                          'United States'])
        print("test_dimgeography_check_completeness_unique_countries_list:", is_passed)
        self.assertTrue(is_passed)

    def test_dimcurrency_currency_name_verify_max_length(self):
        checker = DBChecker()
        output = checker.select_query(f"select CurrencyName from dbo.DimCurrency")
        output_cleared = [i[0] for i in output]
        is_passed = verify_max_length(output_cleared, 40)
        print("test_dimcurrency_currency_name_verify_max_length:", is_passed)
        self.assertTrue(is_passed)

    def test_factfinance_check_average_amount(self):
        checker = DBChecker()
        output = checker.select_query(f"select avg(amount) as avg_value from dbo.FactFinance;")
        is_passed = True if round(output[0][0], 1) == 34475.4 else False
        print("test_factfinance_check_average_amount:", is_passed)
        self.assertTrue(is_passed)

    def test_factfinance_check_min_max(self):
        checker = DBChecker()
        output = checker.select_query(f"select min(amount), max(amount) from dbo.FactFinance;")
        output_cleared = [round(output[0][0], 1), round(output[0][1], 1)]
        output_expected = [-1121918.0, 4820988.0]
        assert all([a == b for a, b in zip(output_cleared, output_expected)])


if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False
    )
