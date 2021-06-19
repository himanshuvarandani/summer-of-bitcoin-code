# Summer Of Bitcoin Code Competition

## Problem Statement
Problem Statement is available in [sb_README.pdf](https://github.com/himanshuvarandani/summer-of-bitcoin-code/blob/main/sb_README.pdf)

## Input
Input is available in [mempool.csv](https://github.com/himanshuvarandani/summer-of-bitcoin-code/blob/main/mempool.csv)

## Code
Code is available in [main.py](https://github.com/himanshuvarandani/summer-of-bitcoin-code/blob/main/main.py)

### Logic
1. We read the input mempool.csv file.
2. We create a dictionary of transactions with keys as txid and values as its data including fee, weight, parents and childs.
3. We have also create a list of tuple with transaction id, fee and weight which is sorted by fee and weight.
4. Now the sorted transactions are selected one by one if it's parent transactions are also selected.
5. If parent transactions are not selected, then the transaction id is added to deselected_transaction.
6. After selecting a transaction, all childs of this transaction are selected if it is deselected before.
7. Before adding a transaction weight of all selected transaction is checked to be less than block weight.
8. Now, transactions are written on block.txt file.

## Output
Output is available in [block.txt](https://github.com/himanshuvarandani/summer-of-bitcoin-code/blob/main/block.txt)
