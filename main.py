from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.models.requests.account_info import AccountInfo
import json


''' Подключение к реестру XRP
'''
JSON_RPC_URL = 'https://s.altnet.rippletest.net:51234/'    # Testnet сети
#JSON_RPC_URL = 'http://localhost:5005/'                    # Свой собственный сервер
#JSON_RPC_URL = 'https://s2.ripple.com:51234/'              # Один из общедоступных серверов
client = JsonRpcClient(JSON_RPC_URL)


''' Создание кошелька
'''
# Генерация кошелька в testnet
test_wallet = generate_faucet_wallet(client, debug=True)

# Создание аккаунта из кошелька
test_account = test_wallet.classic_address

# Получение x-адреса из классического адреса 
# Упаковывает адрес и тег назначения в удобочитаемый формат
test_xadress = addresscodec.classic_address_to_xaddress(test_account, tag=12345, is_test_network=True)

print('Classic adress: ', test_account)
print('X-adress: ', test_xadress)


''' Запрос книги XRP
'''
# Поиск и вывод информации о кошельке, созданном шагом ранее
acct_info = AccountInfo(account=test_account, ledger_index='validated', strict=True)
response = client.request(acct_info)
result = response.result

print('response.status: ', response.status)
print(json.dumps(response.result, indent=4, sort_keys=True))