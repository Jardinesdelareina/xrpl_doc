from xrpl.wallet import Wallet
import xrpl
import json

''' Получение учетных данных
'''
# В seed и sequence указаны тестовые данные
# В производстве необходимо использовать данные существующей учетной записи
test_wallet = Wallet(seed='ssR4o2Mf6U99T6iLwuiL9bokZdx9Z', sequence=31255659)
#print(test_wallet.classic_address)      # rE1Yq6kdWmu3Q8ku361KG3V1omQWqrEYmU

''' Подключение к серверу тестовой сети
'''
testnet_url = 'https://s.altnet.rippletest.net:51234'
client = xrpl.clients.JsonRpcClient(testnet_url)

''' Подготовка транзакции
'''
payment = xrpl.models.transactions.Payment(
    account=test_wallet.classic_address,
    amount=xrpl.utils.xrp_to_drops(1),
    destination='rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe'
)
#print('Объект платежа: ', payment)

''' Подпись транзакции
'''
signed_tx = xrpl.transaction.safe_sign_and_autofill_transaction(payment, test_wallet, client)
max_ledger = signed_tx.last_ledger_sequence
tx_id = signed_tx.get_hash()
#print('Подписанная транзакция: ', signed_tx)
#print('Стоимость сделки (комиссия): ', xrpl.utils.drops_to_xrp(signed_tx.fee), 'XRP')
#print('Экспирация транзакции истекает после: ', max_ledger)
#print('Идентифицирующий хэш: ', tx_id)

''' Отправка транзакции в сеть и проверка ее статуса
'''
try:
    tx_response = xrpl.transaction.send_reliable_submission(signed_tx, client)
except xrpl.transaction.XRPLReliableSubmissionException as e:
    exit(f'Отправка не удалась: {e}')

print(json.dumps(tx_response.result, indent=4, sort_keys=True))
print(f'Ссылка проводник: https://testnet.xrpl.org/transactions/{tx_id}')
metadata = tx_response.result.get('meta', {})
if metadata.get('TransactionResult'):
    print('Результат: ', metadata['TransactionResult'])
if metadata.get('delivered_amount'):
    print('XRP доставлены: ', xrpl.utils.drops_to_xrp(metadata['delivered_amount']))
