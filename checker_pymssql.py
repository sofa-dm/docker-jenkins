import pymssql


class DBChecker:
    def __init__(self):
        self.server = 'host.docker.internal'
        self.database = 'AdventureWorksDW2012'
        self.username = 'DmUser'
        self.password = 'wrefsd1231AWE!'
        self.driver = '{SQL Server}'
        self.port = '1433'
        self.cnn = pymssql.connect(self.server, self.username, self.password, self.database)
        self.cursor = self.cnn.cursor()


    def select_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()


# Auxiliary function. Function prints string description and percent of corrupted rows
def get_result_by_percentage(corrupted_records_amount: int, overall_records_amount: int, description: str) -> bool:
    corrupted_percent = round(corrupted_records_amount / overall_records_amount * 100, 2)
    print(f"{description}, {corrupted_percent}%")
    if corrupted_records_amount == 0:
        return True
    return False


# Test function. Function checks column for only acceptable values
def verify_allowed_values(records: list, allowed_values: list):
    records_amount_with_not_allowed_values = 0
    for i in records:
        if i not in allowed_values:
            records_amount_with_not_allowed_values += 1
    return get_result_by_percentage(records_amount_with_not_allowed_values, len(records),
                                    f"Percentage of records with allowed values ({allowed_values})")


# Test function. Function checks that column doesn't contain any NULL and empty ('') values
def verify_completeness(records: list) -> bool:
    records_amount_with_empty_values = 0
    for i in records:
        if i is None or i == '':
            records_amount_with_empty_values += 1

    return get_result_by_percentage(records_amount_with_empty_values, len(records),
                                    "Percentage of completed records")


# Test function. Function checks that length of values in column have acceptable length
def verify_max_length(records: list, max_length: int):
    records_amount_with_values_more_than_max_length = 0
    for i in records:
        if len(i) > max_length:
            records_amount_with_values_more_than_max_length += 1

    return get_result_by_percentage(records_amount_with_values_more_than_max_length, len(records),
                                    f"Percentage of records with length less than {max_length}")




