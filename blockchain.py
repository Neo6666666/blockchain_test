#start right here!
from functools import reduce
from collections import OrderedDict

from hash_util import hash_block, hash_string_256


MINIG_REWARD = 10
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}

blockchain = [genesis_block]
open_transactions = []
owner = 'Somebody' #TODO change this with unique ID
participants = {'Somebody'} #TODO get set of participants




def get_balance(patricipant):
    """Return balance of given participant."""
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == patricipant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == patricipant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda x, y: x + sum(y) if len(y) > 0 else x + 0, tx_sender, 0)
    #amount_sent =  0 if not reduce(sum, tx_sender) else reduce(sum, tx_sender)[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == patricipant] for block in blockchain]
    amount_recived = reduce(lambda x, y: x + sum(y) if len(y) > 0 else x + 0, tx_recipient, 0)
    #amount_recived = 0 if not reduce(sum, tx_recipient) else reduce(sum, tx_recipient)[0]
    return amount_recived - amount_sent

def get_last_blockchain_val():
    """ Return the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def add_transaction(recipient, sender=owner, amount=0.0):
    """Append a new value as well as the last blockchain value to the blockchain.
    Params:
        -sender: sender of the coins
        -recipient: recipient of the coins 
        -amount: amount of the coins     
    """
    transaction = OrderedDict([
        ('sender', sender), 
        ('recipient', recipient), 
        ('amount', amount)
        ])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def mine_block():
    """Mine new block."""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    reward_transaction = OrderedDict([
        ('sender', 'MINING'),
        ('recipient', owner),
        ('amount', MINIG_REWARD)
    ])
    copy_open_transactions = open_transactions[:]
    copy_open_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copy_open_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True

def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    #print(guess_hash)
    return guess_hash[0:2] == '00'

def proof_of_work():
    last_blockchain = blockchain[-1]
    last_hash = hash_block(last_blockchain)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

def get_transaction_value():
    """Return input of the user (a new transaction amount) as a float."""
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount: '))
    return tx_recipient, tx_amount

def get_user_choice():
    """Prompts the user fot its choice and return it."""
    user_input = input('Your choice: ')
    return user_input

def print_blockchain_elements():
    """Output all blocks of the blockchain."""
    for block in blockchain:
        print(block)
        print('-' * 20)
    else:
        print('=' * 20)

def verify_chain():
    """Verify current blockchain and return True if it's valid. Otherwise False."""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('PoW is invalid.')
            return False
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print('---Choose your action---')
    print('1: Add new transactin value.')
    print('2: Mine a new block.')
    print('3: Output the blockchain.')
    print('4: Output participants.')
    print('5: Check transaction validity.')
    print('h: Manipulate chain.')
    print('q: Quit.')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('New transaction was added!')
        else:
            print('Transaction failed! Error.')
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions is valid.')
        else:
            print('Transactions validation is faled!')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Bob', 'recipient': 'Somebody', 'amount': 10.5}] 
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Invalid input. Try again.')
    if not verify_chain():
        print('ERROR! Chain is not valid!')
        break
    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
print('Goodbye.')