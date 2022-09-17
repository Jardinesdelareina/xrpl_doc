from xrpl.wallet import Wallet
from xrpl.clients import JsonRpcClient

my_wallet = Wallet.create()
print(my_wallet.classic_address)
print(my_wallet.seed)

JSON_RPC_URL = 'https://xrplcluster.com'
#JSON_RPC_URL = 'http://localhost:5005'

client = JsonRpcClient(JSON_RPC_URL)
