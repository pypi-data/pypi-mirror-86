from pagarme import recipient
from pagarme import transaction
from pagarme import transfer
from tests.resources.dictionaries import recipient_dictionary
from tests.resources.dictionaries import transaction_dictionary
from tests.resources.dictionaries import transfer_dictionary


def test_create_recipient():
    _recipient = recipient.create(recipient_dictionary.RECIPIENT)
    assert _recipient['id'] is not None


def test_find_all_recipients():
    all_recipients = recipient.find_all()
    assert all_recipients is not None


def test_find_by():
    _recipient = recipient.create(recipient_dictionary.RECIPIENT)
    search_params = {'id': _recipient['id']}
    find_recipient = recipient.find_by(search_params)
    assert _recipient['id'] == find_recipient[0]['id']


def test_find_default_recipient():
    default_recipient = recipient.default_recipient()['test']
    assert default_recipient is not None


def test_recipient_balance():
    _recipient = recipient.create(recipient_dictionary.RECIPIENT)
    recipient_balance = recipient.recipient_balance(_recipient['id'])
    assert recipient_balance['object'] == 'balance'
    assert recipient_balance['available']['amount'] == 0
    assert recipient_balance['waiting_funds']['amount'] == 0
    assert recipient_balance['transferred']['amount'] == 0


def test_recipient_balance_operation():
    boleto = transaction.create(transaction_dictionary.BOLETO_TRANSACTION_SPLIT_RULE_PERCENTAGE)
    transaction.pay_boleto(boleto['id'], transaction_dictionary.PAY_BOLETO)
    transfer_dictionary.TRANSFER['recipient_id'] = \
        transaction_dictionary.BOLETO_TRANSACTION_SPLIT_RULE_PERCENTAGE['split_rules'][0]['recipient_id']
    _transfer = transfer.create(transfer_dictionary.TRANSFER)
    recipient_balance_operation = recipient.recipient_balance_operation(_transfer['source_id'])
    assert recipient_balance_operation[0]['movement_object']['source_id'] == _transfer['source_id']


def test_recipient_balance_operation_id():
    boleto = transaction.create(transaction_dictionary.BOLETO_TRANSACTION_SPLIT_RULE_PERCENTAGE)
    transaction.pay_boleto(boleto['id'], transaction_dictionary.PAY_BOLETO)
    transfer_dictionary.TRANSFER['recipient_id'] = \
        transaction_dictionary.BOLETO_TRANSACTION_SPLIT_RULE_PERCENTAGE['split_rules'][0]['recipient_id']
    _transfer = transfer.create(transfer_dictionary.TRANSFER)
    recipient_balance_operation = recipient.recipient_balance_operation(_transfer['source_id'])
    recipient_balance_operation_id = \
        recipient.recipient_balance_operation_id(_transfer['source_id'], recipient_balance_operation[0]['id'])
    assert recipient_balance_operation_id['id'] == recipient_balance_operation[0]['id']


def test_update_recipient():
    _recipient = recipient.create(recipient_dictionary.RECIPIENT)
    search_params = {'id': str(_recipient['id'])}
    find_recipient = recipient.find_by(search_params)
    updated_recipient = recipient.update_recipient(find_recipient[0]['id'], recipient_dictionary.UPDATE_RECIPIENT)
    assert find_recipient[0]['transfer_enabled'] != updated_recipient['transfer_enabled']
