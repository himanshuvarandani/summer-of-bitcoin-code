class MempoolTransaction:
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.childs = []
        if parents:
            self.parents = list(parents.split(";"))
        else:
            self.parents = []

    def __str__(self):
        return (
            "===== \nTransaction Id: "
            + self.txid
            + "\nFee: "
            + str(self.fee)
            + "\nWeight: "
            + str(self.weight)
            + "\nChilds: "
            + self.childs.__str__()
            + "\nParents: "
            + self.parents.__str__()
        )


def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open("mempool.csv") as f:
        dict_of_transactions, d1 = {}, {}
        sorted_transactions = []

        # Read all lines and create dictionary of transactions and
        # also a list of transactions sorted by fee and weight
        for line in f.readlines()[1:]:
            (txid, fee, weight, parents) = line.strip().split(",")

            dict_of_transactions[txid] = MempoolTransaction(txid, fee, weight, parents)
            sorted_transactions.append((txid, fee, weight))

            if parents:
                for parent in parents.split(";"):
                    if parent in dict_of_transactions.keys():
                        dict_of_transactions[parent].childs.append(txid)
                    else:
                        d1[parent] = txid
        for parent in d1.keys():
            dict_of_transactions[parent].childs.append(d1[parent])
        sorted_transactions.sort(key=lambda x: ((-1) * x[1], x[2]))
        return (dict_of_transactions, sorted_transactions)


def add_transaction(
    transactions,
    txid,
    selected_transactions,
    deselected_transactions,
    selected_weight,
    block_weight,
):
    """Add txid transaction if it's parent's are already selected"""
    if transactions[txid].parents:
        flag = 0
        for parent in transactions[txid].parents:
            if parent not in selected_transactions:
                flag = 1
                break
        if flag == 0:
            if selected_weight + transactions[txid].weight < block_weight:
                selected_weight += transactions[txid].weight
                selected_transactions.append(txid)

                for child in transactions[txid].childs:
                    if child in deselected_transactions:
                        (
                            selected_transactions,
                            deselected_transactions,
                            selected_weight,
                        ) = add_transaction(
                            transactions,
                            child,
                            selected_transactions,
                            deselected_transactions,
                            selected_weight,
                            block_weight,
                        )
        else:
            deselected_transactions.append(txid)
    else:
        if selected_weight + transactions[txid].weight < block_weight:
            selected_weight += transactions[txid].weight
            selected_transactions.append(txid)
    return (selected_transactions, deselected_transactions, selected_weight)


def main():
    (transactions, sorted_transactions) = parse_mempool_csv()
    selected_transactions, deselected_transactions, selected_weight, block_weight = (
        [],
        [],
        0,
        4000000,
    )
    for transaction in sorted_transactions:
        (
            selected_transactions,
            deselected_transactions,
            selected_weight,
        ) = add_transaction(
            transactions,
            transaction[0],
            selected_transactions,
            deselected_transactions,
            selected_weight,
            block_weight,
        )
    with open("block.txt", "w") as f:
        for txid in selected_transactions:
            f.write(txid + "\n")


if __name__ == "__main__":
    main()
