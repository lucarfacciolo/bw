from datetime import datetime
import pandas as pd


def _business_days_abs_diff(date: datetime, date2: datetime) -> int:
    start = min(date, date2)
    end = max(date, date2)
    days = pd.bdate_range(start, end)  # array of days
    return abs(len(days)) - 1


class Transaction:
    # (NOTE lfacciolo) will compare strings, date is an expection because I want business day functionality

    date: datetime
    department: str
    value: str
    beneficiary: str
    matched: bool

    def __init__(self, row):
        self.date = datetime.strptime(row[0].strip(), "%Y-%m-%d")
        self.department = row[1].strip()
        self.value = row[2].strip()
        self.beneficiary = row[3].strip()
        self.matched = False

    def __lt__(self, transaction: "Transaction"):
        return self.date < transaction.date

    def to_csv(self):
        has_match = "MATCH" if self.matched else "MISSING"
        return [
            self.date.strftime("%Y-%m-%d"),
            self.department,
            self.value,
            self.beneficiary,
            has_match,
        ]

    def is_match(self, transaction: "Transaction") -> bool:
        core_data_match = (
            self.department == transaction.department
            and self.value == transaction.value
            and self.beneficiary == transaction.beneficiary
        )

        # (NOTE lfacciolo) dummy rule here
        # date_diff = abs((self.date - transaction.date).days)

        # (NOTE lfacciolo) considering business days instead, could consider a specific calendar here
        days_constraint = _business_days_abs_diff(self.date, transaction.date) <= 1

        if core_data_match and days_constraint:
            return True
        return False
