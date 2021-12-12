# Creating a blockchain
from _typeshed import Self ## importing the necessary libraries
import datetime
import hashlib   ## one of the pre-requisite is to install postman on your computer
import json
from flask import Flask, jsonify ## have to install flask before, using the terminal

## Building a blockchain
class Blockchain: ## this is the blockchain object created

    def __init__(Self): ## init class function created
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash): ## defining a function to create a single block in the blockchain
        block = {'index': len(self.chain) + 1, 
        'timestamp': str(datetime.datetime.now()),
        'proof':proof,
        'previous hash': previous_hash}

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

# Minning Blockchain

##creating a web app

app = Flask(__name__)

## Creating Blockchain

blockchain = Blockchain()

# Mining a new block

@app.route('/mine_block', methods = ['GET']) ## method define in the flask
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block',
    'index': block['index'],
    'timestamp': block['timestamp'],
    'proof': block['proof'],
    'previous_hash': block['previous_hash']}
    return jsonify(response), 200

## Getting the full Blockchain

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
    'length': len(blockchain.chain)}
    return jsonify(response), 200

## Running the app
app.run(host= '0.0.0.0', port = 5000) ## this is to run the app on postman