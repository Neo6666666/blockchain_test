from uuid import uuid4

from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet


class Node:

    def __init__(self):
        #self.wallet.public_key = str(uuid4()) #TODO uncomment this later
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_value(self):
        """Return input of the user (a new transaction amount) as a float."""
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transaction amount: '))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """Prompts the user fot its choice and return it."""
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        """Output all blocks of the blockchain."""
        for block in self.blockchain.chain:
            print(block)
            print('-' * 20)
        else:
            print('=' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:            
            print('---Choose your action---')
            print('1: Add new transactin value.')
            print('2: Mine a new block.')
            print('3: Output the blockchain.')
            print('4: Check transaction validity.')
            print('5: Create wallet.')
            print('6: Load wallet.')
            print('7: Save wallet.')
            print('q: Quit.')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('New transaction was added!')
                else:
                    print('Transaction failed! Error.')
            elif user_choice == '2':
                if self.blockchain.mine_block():
                    print('Successfully mined.')
                else:
                    print('Mining faled. Got no wallet.')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions is valid.')
                else:
                    print('Transactions validation is faled!')
            elif user_choice =='5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Invalid input. Try again.')
            if not Verification.verify_chain(self.blockchain.chain):
                print('ERROR! Chain is not valid!')
                break
            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
        print('Goodbye.')

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()