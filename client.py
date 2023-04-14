import os
from web3 import Web3
import deploy

abi = deploy.abi
contract_address = deploy.contract_address
deployer = deploy.deployer
private_key = deploy.private_key

# Set up web3 connection
provider_url = os.environ.get("CELO_PROVIDER_URL")
web3 = Web3(Web3.HTTPProvider(provider_url))
assert web3.is_connected(), "Not connected to a Celo node"

# Create an instance of the contract
celo_token = web3.eth.contract(
    address=contract_address, abi=abi)


# Create an instance of the contract
celo_token = web3.eth.contract(address=contract_address, abi=abi)



# Function to transfer tokens
def transfer_tokens(from_account, to_account, value):
    # Get the nonce for the from_account
    nonce = web3.eth.get_transaction_count(from_account)

    # Build the transaction
    transaction = celo_token.functions.transfer(to_account, value).build_transaction({
        'from': from_account,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price,
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt



# Function to purchase tokens
def purchase_tokens(investor, value):
    # Get the nonce for the investor account
    nonce = web3.eth.get_transaction_count(investor)

    # Build the transaction
    transaction = celo_token.functions.purchaseTokens(value).build_transaction({
        'from': investor,
        'nonce': nonce,
        'value': web3.to_wei(value, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.eth.gas_price,
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt



# Transfer tokens
recipient = '0xcdd1151b2bC256103FA2565475e686346CeFd813'
tx_receipt = transfer_tokens(deployer, recipient, 100)
print(
    f"Transfer of 100 tokens from {deployer} to {recipient} completed with transaction hash: {tx_receipt.transactionHash.hex()}")

# Purchase tokens
investor = deployer
tx_receipt = purchase_tokens(investor, 1)
print(
    f"Purchase of 1 ether worth of tokens by {investor} completed with transaction hash: {tx_receipt.transactionHash.hex()}")
