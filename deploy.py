import json
import os
from web3 import Web3
from dotenv import load_dotenv
from solcx import compile_standard, install_solc

load_dotenv()

# Install specific Solidity compiler version
install_solc("0.8.0")


# Set up web3 connection
provider_url = os.environ.get("CELO_PROVIDER_URL")
web3 = Web3(Web3.HTTPProvider(provider_url))
assert web3.is_connected(), "Not connected to a Celo node"

# Set deployer account and private key
deployer = os.environ.get("CELO_DEPLOYER_ADDRESS")
private_key = os.environ.get("CELO_DEPLOYER_PRIVATE_KEY")


with open("CeloToken.sol", "r") as file:
    contract_source_code = file.read()


# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "CeloToken.sol": {
            "content": contract_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
})

# Extract the contract data
contract_data = compiled_sol['contracts']['CeloToken.sol']['CeloToken']
bytecode = contract_data['evm']['bytecode']['object']
abi = json.loads(contract_data['metadata'])['output']['abi']

# Deploy the smart contract
contract = web3.eth.contract(abi=abi, bytecode=bytecode)


nonce = web3.eth.get_transaction_count(deployer)
transaction = {
    'nonce': nonce,
    'gas': 2000000,
    'gasPrice': web3.eth.gas_price,
    'data': bytecode,
}
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

# Get the contract address
contract_address = transaction_receipt['contractAddress']

print(f"Contract deployed at address: {contract_address}")


