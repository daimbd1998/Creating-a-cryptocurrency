## Daim
# Creating a blockchain
from _typeshed import Self ## importing the necessary libraries
import datetime
import hashlib   ## one of the pre-requisite is to install postman on your computer
import json
from flask import Flask, jsonify, request
from flask.wrappers import Response ## have to install flask before, using the terminal
import requests
from uuid import uuid4
from urllib.parse import urlparse
# need to install requests library 'requests==2.18.4: pip install requests==2.18.4'
## Building a blockchain
class Blockchain: ## this is the blockchain object created

    def __init__(Self): ## init class function created
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()

    def create_block(self, proof, previous_hash): ## defining a function to create a single block in the blockchain
        block = {'index': len(self.chain) + 1, 
        'timestamp': str(datetime.datetime.now()),
        'proof':proof,
        'previous hash': previous_hash,
        'transactions': self.transactions}

        self.transactions = [self]
        self.chain.append(block) ## appending the block to the list defined in the init function
        return block

    def get_previous_block(self): ## creating a function to retrieve the previous block
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof ## creating a function for the proof of work

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest() ## using sha256 library to encode hash

    def is_chain_valid(self, chain): ## validating the chain if it is correct or not
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block  = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append ({'sender': sender,
        'reciever': receiver,
        'amount': amount })
        previous_block = self.get_previous_block()
        return previous_block['index' + 1]

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_lenth = len(self.chain)
        for node in network:
            Response = requests.get(f'http://{node}/get_chain') ## node = parsed_url.netloc
            if Response.status_code == 200:
                lenght = Response.json()['length']
                chain = Response.json()['chain']
                if length > max_lenth and slef.is_chain_valid(chain):
                    max_lenth = lenght
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# Minning Blockchain

##creating a web app

app = Flask(__name__)

## creating an adress for the node on the port 5000
node_address = str(uuid4()).replace('-', '')

## Creating Blockchain

blockchain = Blockchain()

# Mining a new block

@app.route('/mine_block', methods = ['GET']) ## method define in the flask, got it from the flask documentation site
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver= 'Daim', amount= 1000)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block',
    'index': block['index'],
    'timestamp': block['timestamp'],
    'proof': block['proof'],
    'previous_hash': block['previous_hash'],
    'transactions': block['transactions']}
    return jsonify(response), 200 ### http status code

## Getting the full Blockchain

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
    'length': len(blockchain.chain)}
    return jsonify(response), 200

## Checking if the blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        Response = {'message':'All good, Blockchain is valid.'}
    else:
        Response = {'message':'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(Response), 201

## Adding a new transaction to the blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'reciever', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400 ### http status code
    index = blockchain.add_transaction(json['sender'], json['reciever'], json['amount'])
    Response = {'message': f'This transaction will be added to block {index}'}
    return jsonify(Response), 201

## Decentralizing the blockchain

######## Connecting to new nodes 
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400 ##### http status code
    for node in nodes:
        blockchain.add_node(node)
    Response = {'message': 'All the nodes are now connected. The Daim Clockchain now contains all the following nodes',
    'total_nodes': list(blockchain.nodes)}
    return jsonify(Response), 201 #### http status code

######## replacing the chain with the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        Response = {'message':'The nodes had different chain so was replaced by the longest one.',
        'new_chain' : blockchain.chain}
    else:
        Response = {'message':'All good. The chain is the largest one.',
        'actual_chain': blockchain.chain}
    return jsonify(Response), 201

## Running the app
app.run(host= '0.0.0.0', port = 5000) ## this is to run the app on postman