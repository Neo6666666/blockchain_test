from time import time


class Block:

    def __init__(self, index:int, previous_hash:str, transactions:list, proof:int, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time

    def __repr__(self):
            return 'Block by index {}, hash {} and proof {}. Transactions is {}'.format(
                self.index, 
                self.previous_hash, 
                self.proof, 
                self.transactions
            )