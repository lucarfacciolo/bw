from typing import List
from transaction import Transaction


def get_transaction_sorted_list(transactions: List) -> List[Transaction]:
    # NOTE(lfacciolo) I have sorted the array to make the logic simpler, this adds a time complexity in our solution. Currently optimizing for maintainability.
    transactions = transactions.copy()  # deep copy
    transactions = [Transaction(row) for row in transactions]
    transactions.sort()
    return transactions
