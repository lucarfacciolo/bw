# external
import csv
from pathlib import Path
from typing import List, Tuple
from pprint import pprint

# internal
from helpers import get_transaction_sorted_list
from transaction import Transaction


def reconcile_accounts(transactions: List, transactions2: List) -> Tuple[List, List]:
    """
    NOTE(lfacciolo)
    this function should check if given a transaction in first list, there is a transaction in list2 in which every parameter is the same, and date has a difference no bigger in absolute, than one.

    Returns a tuple of copies, with one additional columns if record was found or not
    """
    transactions = get_transaction_sorted_list(transactions)
    transactions2 = get_transaction_sorted_list(transactions2)

    for t in transactions:
        for t2 in transactions2:
            if not t2.matched and t.is_match(t2):
                t.matched = True
                t2.matched = True
                break  # NOTE(lfacciolo) no need to iterate over second array after finding first time

    out1 = [t.to_csv() for t in transactions]
    out2 = [t.to_csv() for t in transactions2]

    return (out1, out2)


if __name__ == "__main__":
    try:
        t1 = list(csv.reader(Path("exercise1/transactions1.csv").open()))
        t2 = list(csv.reader(Path("exercise1/transactions2.csv").open()))
        out1, out2 = reconcile_accounts(t1, t2)
        pprint(out1)
        pprint(out2)
    except Exception as e:
        # NOTE(lfacciolo) treat error message here
        raise Exception(f"could not handle files. verify file structure {e}")
