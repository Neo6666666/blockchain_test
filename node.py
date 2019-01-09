from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain


app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app=app)

@app.route('/', methods=['GET',])
def get_ui():
    return send_from_directory('ui', 'node.html')

@app.route('/wallet', methods=['POST',])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'message': 'Wallet created.',
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance(),
        }
        
    else:
        response = {
            'message': 'Can`t save wallet keys.',
        }
    return jsonify(response)

@app.route('/wallet', methods=['GET',])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'message': 'Wallet loaded.',
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance(),
        }
        
    else:
        response = {
            'message': 'Can`t load wallet keys.',
        }
    return jsonify(response)

@app.route('/balance', methods=['GET',])
def get_balance():
    balance = blockchain.get_balance()
    if balance:
        response = {
            'message': 'Balance successfully fetched.',
            'funds': balance,
        }
    else:
        response = {
            'message': 'Can`t find wallet keys.',
            'wallet_set_up': wallet.public_key != None,
        }
    return jsonify(response)

@app.route('/transaction', methods=['POST',])
def add_transaction():
    if wallet.public_key :
        values = request.get_json()
        if values:
            required_fields = ['recipient', 'amount']
            if all(field in values for field in required_fields):
                recipient = values[required_fields[0]]
                amount = values[required_fields[1]]
                signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
                if blockchain.add_transaction(recipient,sender=wallet.public_key, signature=signature, amount=amount):
                    response = {
                    'message': 'Transaction added successfully.',
                    'transaction': {
                        'recipient': recipient,
                        'sender': wallet.public_key,
                        'signature': signature,
                        'amount': amount,
                    },
                    'funds': blockchain.get_balance(),
                }
                else:
                    response = {
                    'message': 'Transaction not valid.',
                }
            else:
                response = {
                'message': 'No requered data found.',
                'fields': values,
            }
        else:
            response = {
                'message': 'No data found.',
            }
    else:
        response = {
                'message': 'No wallet set up.',
            }
    return jsonify(response)

@app.route('/transactions', methods=['GET',])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__.copy() for tx in transactions]
    # response = {
    #     'message': 'Fetched transactions.',
    #     'transactions': dict_transactions,
    # }
    return jsonify(dict_transactions)

@app.route('/mine', methods=['POST',])
def mine():
    block = blockchain.mine_block()
    if block:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__.copy() for tx in dict_block['transactions']]
        response = {
            'message': 'Block successfully mined.',
            'block': dict_block,
            'funds': blockchain.get_balance(),
        }
        return jsonify(response)
    else:
        response = {
            'message': 'Mining failed!',
            'wallet_set_up': wallet.public_key != None,
        }
        return jsonify(response)

@app.route('/chain', methods=['GET',])
def get_chain():
    chain_snapshot = blockchain.chain
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__.copy() for tx in dict_block['transactions']]
    return jsonify(blockchain=dict_chain)

@app.route('/node', methods=['POST',])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached.',
        }
    
    if 'node' not in values:
        response = {
            'message': 'No node data found.',
        }
    else:
        node = values['node']
        blockchain.add_peer_node(node)
        response = {
            'message': 'Node added successfully.',
            'all_nodes': blockchain.get_peeer_nodes(),
        }

    return jsonify(response)

@app.route('/node/<node_url>', methods=['DELETE',])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'Node added successfully.',
        }
    if node_url not in blockchain.get_peeer_nodes():
        response = {
            'message': 'No such node was found.',
        }
    else:
        blockchain.remove_peer_node(node_url)
        response = {
            'message': 'Node deleted successfully.',
            'all_nodes': blockchain.get_peeer_nodes(),
        }
    return jsonify(response)

@app.route('/nodes', methods=['GET',])
def get_nodes():
    nodes = blockchain.get_peeer_nodes()
    response = {
            'all_nodes': nodes,
        }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)