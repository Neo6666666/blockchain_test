import json
from functools import reduce
from collections import OrderedDict

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification


MINIG_REWARD = 10



class Blockchain:

    def __init__(self, node_id):
        # Initialize first block
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing empty blockchain list
        self.__chain = [genesis_block,]
        # Unhandled transactions
        self.__open_transactions = []
        self.load_data()
        self.host_node_id = node_id

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:

                    updated_transactions = list()
                    for tx in block['transactions']:
                        updated_transactions.append(Transaction(
                            tx['sender'],
                            tx['recipient'],
                            tx['amount']
                        ))

                    
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        updated_transactions,
                        block['proof'],
                        block['timestamp']
                    )

                    updated_blockchain.append(updated_block)

                self.__chain = updated_blockchain

                open_transactions = json.loads(file_content[1])

                updated_open_transactions = list()
                for tx in open_transactions:
                    updated_open_transactions.append(Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['amount']
                    ))

                self.open_transactions = updated_open_transactions
        except (IOError, IndexError):
            print("Error hapens while loading! No blockchain file or wrong chain of blocks.")


    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_block = [block.__dict__ for block in [
                        Block(blk.index, blk.previous_hash, [
                            tx.__dict__ for tx in blk.transactions
                        ] , blk.proof, blk.timestamp) for blk in self.__chain
                    ]
                ]
                f.write(json.dumps(saveable_block))
                f.flush()
                f.write('\n')
                f.flush()
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
                f.flush()
        except IOError:
            print('Saving error.')
    
    def proof_of_work(self):
        last_blockchain = self.__chain[-1]
        last_hash = hash_block(last_blockchain)
        proof = 0
        while not Verification.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        """Return balance of hosted node."""
        patricipant = self.host_node_id
        
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == patricipant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == patricipant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda x, y: x + sum(y) if len(y) > 0 else x + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == patricipant] for block in self.__chain]
        amount_recived = reduce(lambda x, y: x + sum(y) if len(y) > 0 else x + 0, tx_recipient, 0)
        return amount_recived - amount_sent

    def get_last_blockchain_val(self):
        """ Return the last value of the current blockchain."""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, amount=0.0):
        """Append a new value as well as the last blockchain value to the blockchain.
        Params:
            -sender: sender of the coins
            -recipient: recipient of the coins 
            -amount: amount of the coins     
        """
        transaction = Transaction(
            sender,
            recipient,
            amount
        )

        if Verification.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """Mine new block."""
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction('MINING', self.host_node_id, MINIG_REWARD)

        copy_open_transactions = self.open_transactions[:]
        copy_open_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copy_open_transactions, proof)

        self.__chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True

















